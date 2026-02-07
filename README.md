<div align="center">
  <img src="nanobot_logo.png" alt="nanobot" width="500">
  <h1>Nanobot: Ultra-Lightweight Personal AI Assistant with Web UI</h1>
  <p>
    <img src="https://img.shields.io/badge/python-≥3.11-blue" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
    <img src="https://img.shields.io/badge/web_ui-enabled-brightgreen" alt="Web UI">
  </p>
</div>

🐈 **Nanobot** is an **ultra-lightweight** personal AI assistant with a modern web interface 

⚡️ Delivers core agent functionality in just **~4,000** lines of code — **99% smaller** than Clawdbot's 430k+ lines.

📏 Real-time line count: **3,390 lines** (run `bash core_agent_lines.sh` to verify anytime)

## 📢 What's New

- **🌐 Modern Web UI** - Beautiful dark-themed chat interface (ChatGPT-style)
- **⚙️ Settings Page** - Easy configuration for Telegram, WhatsApp, Discord, Feishu
- **🎨 Professional Design** - Clean, responsive, and user-friendly
- **📱 Multi-Platform** - Connect via web browser or messaging apps
- **🚀 One-Click Setup** - Configure everything through the web interface

## Key Features:

🌐 **Modern Web UI**: Beautiful chat interface with settings page for easy configuration

🪶 **Ultra-Lightweight**: Just ~3,400 lines of core agent code

⚡️ **Lightning Fast**: Minimal footprint, faster startup, lower resource usage

💎 **Easy Setup**: Configure everything through the web interface

📱 **Multi-Platform**: Telegram, WhatsApp, Discord, Feishu support

🎨 **Professional Design**: Dark theme, responsive layout, ChatGPT-style interface

## 🏗️ Architecture

<p align="center">
  <img src="nanobot_arch.png" alt="nanobot architecture" width="800">
</p>

## ✨ Features

<table align="center">
  <tr align="center">
    <th><p align="center">📈 24/7 Real-Time Market Analysis</p></th>
    <th><p align="center">🚀 Full-Stack Software Engineer</p></th>
    <th><p align="center">📅 Smart Daily Routine Manager</p></th>
    <th><p align="center">📚 Personal Knowledge Assistant</p></th>
  </tr>
  <tr>
    <td align="center"><p align="center"><img src="case/search.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/code.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/scedule.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/memory.gif" width="180" height="400"></p></td>
  </tr>
  <tr>
    <td align="center">Discovery • Insights • Trends</td>
    <td align="center">Develop • Deploy • Scale</td>
    <td align="center">Schedule • Automate • Organize</td>
    <td align="center">Learn • Memory • Reasoning</td>
  </tr>
</table>

## 📦 Install

**Install from source** (recommended)

```bash
git clone https://github.com/saquantsystem-ops/nanochat.git
cd nanochat
pip install -e .
```

## 🚀 Quick Start

### Option 1: Web UI (Recommended) 🌐

**1. Initialize**
```bash
nanobot onboard
```

**2. Start Web UI**
```bash
nanobot webui
```

**3. Open Browser**
- Main Chat: http://127.0.0.1:8080
- Settings: http://127.0.0.1:8080/settings

**4. Configure**
- Go to Settings page
- Add your OpenAI/OpenRouter API key
- Choose your model (e.g., gpt-4o-mini)
- Save and start chatting!

### Option 2: Command Line

**1. Initialize**
```bash
nanobot onboard
```

**2. Add API Key** (edit `~/.nanobot/config.json`)
```json
{
  "providers": {
    "openai": {
      "apiKey": "sk-..."
    }
  },
  "agents": {
    "defaults": {
      "model": "gpt-4o-mini"
    }
  }
}
```

**3. Chat**
```bash
nanobot agent -m "Hello!"
```

## 🖥️ Local Models (vLLM)

Run nanobot with your own local models using vLLM or any OpenAI-compatible server.

**1. Start your vLLM server**

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000
```

**2. Configure** (`~/.nanobot/config.json`)

```json
{
  "providers": {
    "vllm": {
      "apiKey": "dummy",
      "apiBase": "http://localhost:8000/v1"
    }
  },
  "agents": {
    "defaults": {
      "model": "meta-llama/Llama-3.1-8B-Instruct"
    }
  }
}
```

**3. Chat**

```bash
nanobot agent -m "Hello from my local LLM!"
```

> [!TIP]
> The `apiKey` can be any non-empty string for local servers that don't require authentication.

## 💬 Connect Messaging Apps

Configure everything through the **Settings Page** (http://127.0.0.1:8080/settings)

| Channel | Setup Difficulty | Configuration |
|---------|-----------------|---------------|
| **Telegram** | ⭐ Easy | Bot token + User IDs |
| **Discord** | ⭐ Easy | Bot token + User IDs |
| **WhatsApp** | ⭐⭐ Medium | Phone numbers + QR scan |
| **Feishu** | ⭐⭐ Medium | App ID + Secret |

<details>
<summary><b>Telegram</b> (Recommended)</summary>

**1. Create a bot**
- Open Telegram, search `@BotFather`
- Send `/newbot`, follow prompts
- Copy the token

**2. Configure**

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

> Get your user ID from `@userinfobot` on Telegram.

**3. Run**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Discord</b></summary>

**1. Create a bot**
- Go to https://discord.com/developers/applications
- Create an application → Bot → Add Bot
- Copy the bot token

**2. Enable intents**
- In the Bot settings, enable **MESSAGE CONTENT INTENT**
- (Optional) Enable **SERVER MEMBERS INTENT** if you plan to use allow lists based on member data

**3. Get your User ID**
- Discord Settings → Advanced → enable **Developer Mode**
- Right-click your avatar → **Copy User ID**

**4. Configure**

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

**5. Invite the bot**
- OAuth2 → URL Generator
- Scopes: `bot`
- Bot Permissions: `Send Messages`, `Read Message History`
- Open the generated invite URL and add the bot to your server

**6. Run**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>WhatsApp</b></summary>

Requires **Node.js ≥18**.

**1. Link device**

```bash
nanobot channels login
# Scan QR with WhatsApp → Settings → Linked Devices
```

**2. Configure**

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+1234567890"]
    }
  }
}
```

**3. Run** (two terminals)

```bash
# Terminal 1
nanobot channels login

# Terminal 2
nanobot gateway
```

</details>

<details>
<summary><b>Feishu (飞书)</b></summary>

Uses **WebSocket** long connection — no public IP required.

```bash
pip install nanobot-ai[feishu]
```

**1. Create a Feishu bot**
- Visit [Feishu Open Platform](https://open.feishu.cn/app)
- Create a new app → Enable **Bot** capability
- **Permissions**: Add `im:message` (send messages)
- **Events**: Add `im.message.receive_v1` (receive messages)
  - Select **Long Connection** mode (requires running nanobot first to establish connection)
- Get **App ID** and **App Secret** from "Credentials & Basic Info"
- Publish the app

**2. Configure**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "encryptKey": "",
      "verificationToken": "",
      "allowFrom": []
    }
  }
}
```

> `encryptKey` and `verificationToken` are optional for Long Connection mode.
> `allowFrom`: Leave empty to allow all users, or add `["ou_xxx"]` to restrict access.

**3. Run**

```bash
nanobot gateway
```

> [!TIP]
> Feishu uses WebSocket to receive messages — no webhook or public IP needed!

</details>

## ⚙️ Configuration

Config file: `~/.nanobot/config.json`

### Providers

> [!NOTE]
> Groq provides free voice transcription via Whisper. If configured, Telegram voice messages will be automatically transcribed.

| Provider | Purpose | Get API Key |
|----------|---------|-------------|
| `openrouter` | LLM (recommended, access to all models) | [openrouter.ai](https://openrouter.ai) |
| `anthropic` | LLM (Claude direct) | [console.anthropic.com](https://console.anthropic.com) |
| `openai` | LLM (GPT direct) | [platform.openai.com](https://platform.openai.com) |
| `deepseek` | LLM (DeepSeek direct) | [platform.deepseek.com](https://platform.deepseek.com) |
| `groq` | LLM + **Voice transcription** (Whisper) | [console.groq.com](https://console.groq.com) |
| `gemini` | LLM (Gemini direct) | [aistudio.google.com](https://aistudio.google.com) |


<details>
<summary><b>Full config example</b></summary>

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    }
  },
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    },
    "groq": {
      "apiKey": "gsk_xxx"
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "123456:ABC...",
      "allowFrom": ["123456789"]
    },
    "discord": {
      "enabled": false,
      "token": "YOUR_DISCORD_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    },
    "whatsapp": {
      "enabled": false
    },
    "feishu": {
      "enabled": false,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "encryptKey": "",
      "verificationToken": "",
      "allowFrom": []
    }
  },
  "tools": {
    "web": {
      "search": {
        "apiKey": "BSA..."
      }
    }
  }
}
```

</details>

## CLI Reference

| Command | Description |
|---------|-------------|
| `nanobot onboard` | Initialize config & workspace |
| `nanobot webui` | **Start Web UI** (http://127.0.0.1:8080) |
| `nanobot agent -m "..."` | Chat with the agent (CLI) |
| `nanobot agent` | Interactive chat mode (CLI) |
| `nanobot gateway` | Start messaging gateway |
| `nanobot status` | Show status |
| `nanobot channels login` | Link WhatsApp (scan QR) |

<details>
<summary><b>Scheduled Tasks (Cron)</b></summary>

```bash
# Add a job
nanobot cron add --name "daily" --message "Good morning!" --cron "0 9 * * *"
nanobot cron add --name "hourly" --message "Check status" --every 3600

# List jobs
nanobot cron list

# Remove a job
nanobot cron remove <job_id>
```

</details>

## 🐳 Docker

> [!TIP]
> The `-v ~/.nanobot:/root/.nanobot` flag mounts your local config directory into the container, so your config and workspace persist across container restarts.

Build and run nanobot in a container:

```bash
# Build the image
docker build -t nanobot .

# Initialize config (first time only)
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot onboard

# Edit config on host to add API keys
vim ~/.nanobot/config.json

# Run gateway (connects to Telegram/WhatsApp)
docker run -v ~/.nanobot:/root/.nanobot -p 18790:18790 nanobot gateway

# Or run a single command
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot agent -m "Hello!"
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot status
```

## 📁 Project Structure

```
nanobot/
├── web/            # 🌐 Web UI (NEW!)
│   ├── server.py   #    Web server
│   └── static/     #    HTML, CSS, JS
├── agent/          # 🧠 Core agent logic
│   ├── loop.py     #    Agent loop (LLM ↔ tool execution)
│   ├── context.py  #    Prompt builder
│   ├── memory.py   #    Persistent memory
│   └── tools/      #    Built-in tools
├── skills/         # 🎯 Bundled skills (github, weather, tmux...)
├── channels/       # 📱 Telegram, Discord, WhatsApp, Feishu
├── providers/      # 🤖 LLM providers (OpenAI, OpenRouter, etc.)
├── cron/           # ⏰ Scheduled tasks
└── cli/            # 🖥️ Commands
```

## 🤝 Roadmap

- [x] **Modern Web UI** — Beautiful chat interface with settings page
- [x] **Multi-Platform** — Telegram, Discord, WhatsApp, Feishu support
- [ ] **Enhanced Web UI** — Real-time gateway control, QR code display
- [ ] **Multi-modal** — Image and voice support
- [ ] **Long-term memory** — Persistent context across sessions
- [ ] **Plugin System** — Easy extension mechanism

---

<p align="center">
  <sub>Built with ❤️ for the AI community</sub>
</p>
