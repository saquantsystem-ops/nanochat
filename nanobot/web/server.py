"""
Web UI server for nanobot
Provides a browser-based interface for configuration and chat
"""
import asyncio
import json
from pathlib import Path
from typing import Any

from aiohttp import web
from loguru import logger

from nanobot.agent.loop import AgentLoop
from nanobot.bus.events import InboundMessage, OutboundMessage
from nanobot.bus.queue import MessageBus
from nanobot.config.loader import load_config
from nanobot.providers.litellm_provider import LiteLLMProvider
from nanobot.session.manager import SessionManager


class WebUIServer:
    """Web UI server for nanobot"""

    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.bus = MessageBus()
        self.sessions: dict[str, SessionManager] = {}
        self.agent_tasks: dict[str, asyncio.Task] = {}
        
        # Setup routes
        self._setup_routes()

    def _setup_routes(self):
        """Setup HTTP routes"""
        self.app.router.add_get("/", self.index)
        self.app.router.add_get("/settings", self.settings_page)
        self.app.router.add_get("/api/config", self.get_config)
        self.app.router.add_post("/api/config", self.update_config)
        self.app.router.add_post("/api/chat", self.chat)
        self.app.router.add_get("/api/status", self.status)
        self.app.router.add_get("/ws", self.websocket_handler)
        
        # Settings APIs
        self.app.router.add_get("/api/settings", self.get_settings)
        self.app.router.add_post("/api/settings/telegram", self.save_telegram)
        self.app.router.add_post("/api/settings/whatsapp", self.save_whatsapp)
        self.app.router.add_post("/api/settings/discord", self.save_discord)
        self.app.router.add_post("/api/settings/feishu", self.save_feishu)
        self.app.router.add_get("/api/test/telegram", self.test_telegram)
        self.app.router.add_get("/api/test/discord", self.test_discord)
        self.app.router.add_get("/api/test/feishu", self.test_feishu)
        self.app.router.add_get("/api/whatsapp/qr", self.whatsapp_qr)
        self.app.router.add_post("/api/gateway/start", self.start_gateway)
        self.app.router.add_post("/api/gateway/stop", self.stop_gateway)
        self.app.router.add_get("/api/gateway/status", self.gateway_status)
        
        # Static files
        static_dir = Path(__file__).parent / "static"
        if static_dir.exists():
            self.app.router.add_static("/static", static_dir)

    async def index(self, request: web.Request) -> web.Response:
        """Serve the main HTML page"""
        html_file = Path(__file__).parent / "static" / "index.html"
        if html_file.exists():
            return web.FileResponse(html_file)
        return web.Response(text=self._get_default_html(), content_type="text/html")
    
    async def settings_page(self, request: web.Request) -> web.Response:
        """Serve the settings page"""
        html_file = Path(__file__).parent / "static" / "settings.html"
        if html_file.exists():
            return web.FileResponse(html_file)
        return web.Response(text="Settings page not found", status=404)

    async def get_config(self, request: web.Request) -> web.Response:
        """Get current configuration (sanitized)"""
        try:
            config = load_config()
            # Sanitize sensitive data
            safe_config = {
                "agents": config.agents.model_dump(),
                "providers": {
                    name: {"configured": bool(prov.api_key)}
                    for name, prov in config.providers.items()
                },
                "tools": config.tools.model_dump() if config.tools else {}
            }
            return web.json_response(safe_config)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def update_config(self, request: web.Request) -> web.Response:
        """Update configuration"""
        try:
            data = await request.json()
            config_path = Path.home() / ".nanobot" / "config.json"
            
            # Load existing config
            with open(config_path, "r") as f:
                config = json.load(f)
            
            # Update with new data
            if "provider" in data and "apiKey" in data:
                provider = data["provider"]
                if provider in config["providers"]:
                    config["providers"][provider]["apiKey"] = data["apiKey"]
            
            if "model" in data:
                config["agents"]["defaults"]["model"] = data["model"]
            
            # Save config
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            
            return web.json_response({"success": True})
        except Exception as e:
            logger.error(f"Error updating config: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def chat(self, request: web.Request) -> web.Response:
        """Handle chat messages"""
        try:
            data = await request.json()
            message = data.get("message", "")
            session_id = data.get("session_id", "web:default")
            
            if not message:
                return web.json_response({"error": "Message is required"}, status=400)
            
            # Create or get session
            if session_id not in self.sessions:
                self.sessions[session_id] = SessionManager()
            
            # Send message to agent
            inbound = InboundMessage(
                channel="web",
                chat_id=session_id,
                user_id="web-user",
                text=message,
                timestamp=0
            )
            
            # Process with agent
            config = load_config()
            provider = LiteLLMProvider(config=config)
            agent = AgentLoop(
                provider=provider,
                session_manager=self.sessions[session_id],
                config=config,
                bus=self.bus
            )
            
            response = await agent._process_message(inbound)
            
            return web.json_response({
                "response": response,
                "session_id": session_id
            })
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def status(self, request: web.Request) -> web.Response:
        """Get server status"""
        try:
            config = load_config()
            return web.json_response({
                "status": "running",
                "model": config.agents.defaults.model,
                "sessions": len(self.sessions)
            })
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def websocket_handler(self, request: web.Request) -> web.WebSocketResponse:
        """WebSocket handler for real-time chat"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        session_id = f"web:{id(ws)}"
        self.sessions[session_id] = SessionManager()
        
        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    message = data.get("message", "")
                    
                    # Process message
                    config = load_config()
                    provider = LiteLLMProvider(config=config)
                    agent = AgentLoop(
                        provider=provider,
                        session_manager=self.sessions[session_id],
                        config=config,
                        bus=self.bus
                    )
                    
                    inbound = InboundMessage(
                        channel="web",
                        chat_id=session_id,
                        user_id="web-user",
                        text=message,
                        timestamp=0
                    )
                    
                    response = await agent._process_message(inbound)
                    await ws.send_json({"response": response})
                    
        finally:
            if session_id in self.sessions:
                del self.sessions[session_id]
        
        return ws

    def _get_default_html(self) -> str:
        """Get default HTML if static file doesn't exist"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>🐈 Nanobot Web UI</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h1>🐈 Nanobot Web UI</h1>
    <p>Static files not found. Please create static/index.html</p>
</body>
</html>
"""

    async def start(self):
        """Start the web server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        logger.info(f"🌐 Web UI running at http://{self.host}:{self.port}")
        
        # Keep running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Shutting down web UI...")
        finally:
            await runner.cleanup()
    
    async def get_settings(self, request: web.Request) -> web.Response:
        """Get all channel settings"""
        try:
            config_path = Path.home() / ".nanobot" / "config.json"
            with open(config_path, "r") as f:
                config = json.load(f)
            
            return web.json_response({
                "telegram": config.get("channels", {}).get("telegram", {}),
                "whatsapp": config.get("channels", {}).get("whatsapp", {}),
                "discord": config.get("channels", {}).get("discord", {}),
                "feishu": config.get("channels", {}).get("feishu", {})
            })
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def save_telegram(self, request: web.Request) -> web.Response:
        """Save Telegram settings"""
        try:
            data = await request.json()
            config_path = Path.home() / ".nanobot" / "config.json"
            
            with open(config_path, "r") as f:
                config = json.load(f)
            
            if "channels" not in config:
                config["channels"] = {}
            if "telegram" not in config["channels"]:
                config["channels"]["telegram"] = {}
            
            config["channels"]["telegram"]["enabled"] = data.get("enabled", False)
            config["channels"]["telegram"]["token"] = data.get("token", "")
            config["channels"]["telegram"]["allowFrom"] = data.get("allowFrom", [])
            
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            
            return web.json_response({"success": True})
        except Exception as e:
            logger.error(f"Error saving Telegram settings: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def save_whatsapp(self, request: web.Request) -> web.Response:
        """Save WhatsApp settings"""
        try:
            data = await request.json()
            config_path = Path.home() / ".nanobot" / "config.json"
            
            with open(config_path, "r") as f:
                config = json.load(f)
            
            if "channels" not in config:
                config["channels"] = {}
            if "whatsapp" not in config["channels"]:
                config["channels"]["whatsapp"] = {}
            
            config["channels"]["whatsapp"]["enabled"] = data.get("enabled", False)
            config["channels"]["whatsapp"]["allowFrom"] = data.get("allowFrom", [])
            
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            
            return web.json_response({"success": True})
        except Exception as e:
            logger.error(f"Error saving WhatsApp settings: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def save_discord(self, request: web.Request) -> web.Response:
        """Save Discord settings"""
        try:
            data = await request.json()
            config_path = Path.home() / ".nanobot" / "config.json"
            
            with open(config_path, "r") as f:
                config = json.load(f)
            
            if "channels" not in config:
                config["channels"] = {}
            if "discord" not in config["channels"]:
                config["channels"]["discord"] = {}
            
            config["channels"]["discord"]["enabled"] = data.get("enabled", False)
            config["channels"]["discord"]["token"] = data.get("token", "")
            config["channels"]["discord"]["allowFrom"] = data.get("allowFrom", [])
            
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            
            return web.json_response({"success": True})
        except Exception as e:
            logger.error(f"Error saving Discord settings: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def save_feishu(self, request: web.Request) -> web.Response:
        """Save Feishu settings"""
        try:
            data = await request.json()
            config_path = Path.home() / ".nanobot" / "config.json"
            
            with open(config_path, "r") as f:
                config = json.load(f)
            
            if "channels" not in config:
                config["channels"] = {}
            if "feishu" not in config["channels"]:
                config["channels"]["feishu"] = {}
            
            config["channels"]["feishu"]["enabled"] = data.get("enabled", False)
            config["channels"]["feishu"]["appId"] = data.get("appId", "")
            config["channels"]["feishu"]["appSecret"] = data.get("appSecret", "")
            config["channels"]["feishu"]["allowFrom"] = data.get("allowFrom", [])
            
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            
            return web.json_response({"success": True})
        except Exception as e:
            logger.error(f"Error saving Feishu settings: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def test_telegram(self, request: web.Request) -> web.Response:
        """Test Telegram connection"""
        try:
            config_path = Path.home() / ".nanobot" / "config.json"
            with open(config_path, "r") as f:
                config = json.load(f)
            
            token = config.get("channels", {}).get("telegram", {}).get("token", "")
            if not token or ":" not in token:
                return web.json_response({"success": False, "error": "Invalid token format"})
            
            return web.json_response({"success": True, "message": "Token format is valid"})
        except Exception as e:
            return web.json_response({"success": False, "error": str(e)})
    
    async def test_discord(self, request: web.Request) -> web.Response:
        """Test Discord connection"""
        try:
            config_path = Path.home() / ".nanobot" / "config.json"
            with open(config_path, "r") as f:
                config = json.load(f)
            
            token = config.get("channels", {}).get("discord", {}).get("token", "")
            if not token:
                return web.json_response({"success": False, "error": "No token provided"})
            
            return web.json_response({"success": True, "message": "Token is set"})
        except Exception as e:
            return web.json_response({"success": False, "error": str(e)})
    
    async def test_feishu(self, request: web.Request) -> web.Response:
        """Test Feishu connection"""
        try:
            config_path = Path.home() / ".nanobot" / "config.json"
            with open(config_path, "r") as f:
                config = json.load(f)
            
            feishu = config.get("channels", {}).get("feishu", {})
            if not feishu.get("appId") or not feishu.get("appSecret"):
                return web.json_response({"success": False, "error": "App ID or Secret missing"})
            
            return web.json_response({"success": True, "message": "Credentials are set"})
        except Exception as e:
            return web.json_response({"success": False, "error": str(e)})
    
    async def whatsapp_qr(self, request: web.Request) -> web.Response:
        """Get WhatsApp QR code"""
        try:
            # Start the WhatsApp bridge and get QR code
            import subprocess
            import asyncio
            
            # Check if Node.js is installed
            try:
                result = subprocess.run(['node', '--version'], capture_output=True, text=True)
                if result.returncode != 0:
                    return web.json_response({
                        "success": False,
                        "error": "Node.js is not installed. Please install Node.js ≥18 to use WhatsApp."
                    })
            except FileNotFoundError:
                return web.json_response({
                    "success": False,
                    "error": "Node.js is not installed. Please install Node.js ≥18 to use WhatsApp."
                })
            
            # For now, provide instructions
            return web.json_response({
                "success": False,
                "qr": None,
                "message": "To connect WhatsApp, please run this command in a separate terminal:",
                "command": "nanobot channels login",
                "instructions": [
                    "1. Open a new terminal/command prompt",
                    "2. Run: nanobot channels login",
                    "3. A QR code will appear in the terminal",
                    "4. Scan it with WhatsApp on your phone",
                    "5. Go to Settings → Linked Devices → Link a Device",
                    "6. Scan the QR code"
                ]
            })
        except Exception as e:
            logger.error(f"Error generating WhatsApp QR: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def start_gateway(self, request: web.Request) -> web.Response:
        """Start the gateway"""
        try:
            return web.json_response({
                "success": False,
                "error": "Gateway control from web UI is not yet implemented. Please run 'nanobot gateway' in terminal."
            })
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def stop_gateway(self, request: web.Request) -> web.Response:
        """Stop the gateway"""
        try:
            return web.json_response({
                "success": False,
                "error": "Gateway control from web UI is not yet implemented."
            })
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def gateway_status(self, request: web.Request) -> web.Response:
        """Get gateway status"""
        try:
            return web.json_response({"status": "stopped"})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)


async def run_web_ui(host: str = "127.0.0.1", port: int = 8080):
    """Run the web UI server"""
    server = WebUIServer(host, port)
    await server.start()
