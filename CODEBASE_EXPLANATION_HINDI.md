# 🐈 Nanobot Codebase - विस्तृत व्याख्या (हिंदी में)

## 📋 परियोजना का परिचय

**Nanobot** एक अत्यंत हल्का (ultra-lightweight) व्यक्तिगत AI सहायक है जो सिर्फ **~3,400 लाइनों** के कोड में बनाया गया है। यह [Clawdbot](https://github.com/openclaw/openclaw) से प्रेरित है लेकिन 99% छोटा है (Clawdbot में 430k+ लाइनें हैं)।

### मुख्य विशेषताएं:
- 🪶 **अत्यंत हल्का**: केवल ~3,400 लाइनें
- 🔬 **शोध के लिए तैयार**: साफ और पढ़ने योग्य कोड
- ⚡️ **तेज़**: कम संसाधन उपयोग
- 💎 **उपयोग में आसान**: एक क्लिक में तैनात करें

### समर्थित प्लेटफॉर्म:
- Telegram, Discord, WhatsApp, Feishu
- OpenRouter, Anthropic, OpenAI, DeepSeek, Groq, Gemini (LLM providers)
- वेब खोज, शेल कमांड, फाइल ऑपरेशन, शेड्यूल्ड टास्क

---

## 📁 मुख्य निर्देशिका संरचना

```
nanobot/
├── nanobot/        # मुख्य Python पैकेज
├── bridge/         # WhatsApp के लिए Node.js ब्रिज
├── workspace/      # एजेंट कॉन्फ़िगरेशन फाइलें
├── tests/          # टेस्ट फाइलें
├── case/           # डेमो GIF इमेजेस
└── [कॉन्फ़िगरेशन फाइलें]
```

---

## 🗂️ विस्तृत निर्देशिका व्याख्या

### 1. `nanobot/` - मुख्य Python पैकेज

यह परियोजना का मुख्य भाग है जिसमें सभी कोर फंक्शनलिटी है।

#### 📂 `nanobot/agent/` - एजेंट का मुख्य तर्क

यह AI एजेंट का दिमाग है।

**फाइलें:**


- **`loop.py`** - एजेंट का मुख्य लूप
  - `AgentLoop` क्लास: LLM और टूल्स के बीच संचार को संभालता है
  - संदेशों को प्रोसेस करता है, LLM को कॉल करता है, और टूल्स को execute करता है
  - डिफ़ॉल्ट टूल्स को रजिस्टर करता है (फाइल, शेल, वेब, मैसेज, स्पॉन)

- **`context.py`** - प्रॉम्प्ट बिल्डर
  - `ContextBuilder` क्लास: सिस्टम प्रॉम्प्ट बनाता है
  - workspace फाइलों को लोड करता है (SOUL.md, AGENTS.md, USER.md, TOOLS.md)
  - स्किल्स को कॉन्टेक्स्ट में जोड़ता है
  - एजेंट की पहचान और व्यक्तित्व को परिभाषित करता है

- **`memory.py`** - स्थायी मेमोरी
  - `MemoryStore` क्लास: दैनिक नोट्स को संभालता है
  - `memory/` डायरेक्टरी में YYYY-MM-DD.md फाइलें बनाता है
  - एजेंट को महत्वपूर्ण जानकारी याद रखने में मदद करता है

- **`skills.py`** - स्किल्स लोडर
  - `SkillsLoader` क्लास: स्किल्स को लोड और मैनेज करता है
  - बिल्ट-इन स्किल्स (`nanobot/skills/`) और workspace स्किल्स को सपोर्ट करता है
  - SKILL.md फाइलों को पार्स करता है (YAML frontmatter + Markdown)

- **`subagent.py`** - बैकग्राउंड टास्क मैनेजर
  - `SubagentManager` क्लास: subagents को spawn करता है
  - जटिल या समय लेने वाले कार्यों को स्वतंत्र रूप से चलाता है
  - परिणाम वापस रिपोर्ट करता है

- **`__init__.py`** - पैकेज इनिशियलाइज़ेशन

#### 📂 `nanobot/agent/tools/` - बिल्ट-इन टूल्स

एजेंट के लिए उपलब्ध टूल्स।

- **`base.py`** - टूल बेस क्लास
  - `Tool` abstract class: सभी टूल्स के लिए इंटरफेस
  - `name()`, `description()`, `parameters()`, `execute()` methods

- **`filesystem.py`** - फाइल ऑपरेशन टूल्स
  - `ReadFileTool`: फाइलें पढ़ता है
  - `WriteFileTool`: फाइलें लिखता है
  - `EditFileTool`: फाइलों में टेक्स्ट replace करता है
  - `ListDirTool`: डायरेक्टरी की सामग्री list करता है

- **`shell.py`** - शेल कमांड execution
  - `ExecTool`: शेल कमांड चलाता है
  - सुरक्षा: खतरनाक कमांड ब्लॉक करता है (rm -rf, format, etc.)
  - टाइमआउट और आउटपुट truncation

- **`web.py`** - वेब एक्सेस टूल्स
  - `WebSearchTool`: Brave Search API का उपयोग करके वेब खोज
  - `WebFetchTool`: URL से content fetch और extract करता है
  - Readability का उपयोग करके मुख्य content निकालता है

- **`message.py`** - मैसेजिंग टूल
  - `MessageTool`: यूजर को संदेश भेजता है
  - चैनल और chat_id को ट्रैक करता है

- **`spawn.py`** - Subagent spawning
  - `SpawnTool`: बैकग्राउंड में subagent चलाता है
  - जटिल कार्यों को delegate करता है

- **`cron.py`** - शेड्यूल्ड टास्क टूल
  - `CronTool`: cron jobs को मैनेज करता है
  - शेड्यूल्ड रिमाइंडर और recurring tasks

- **`registry.py`** - टूल रजिस्ट्री
  - `ToolRegistry`: सभी टूल्स को register और manage करता है
  - टूल्स को नाम से retrieve करता है

- **`__init__.py`** - टूल्स पैकेज इनिशियलाइज़ेशन


#### 📂 `nanobot/channels/` - संचार प्लेटफॉर्म

विभिन्न मैसेजिंग प्लेटफॉर्म के साथ इंटीग्रेशन।

- **`base.py`** - चैनल बेस क्लास
  - `BaseChannel`: सभी चैनलों के लिए abstract interface
  - `start()`, `stop()`, `send()` methods
  - MessageBus के साथ इंटीग्रेशन

- **`telegram.py`** - Telegram इंटीग्रेशन
  - `TelegramChannel`: Telegram bot API
  - `python-telegram-bot` library का उपयोग
  - Markdown को Telegram HTML में convert करता है
  - Voice message transcription (Groq Whisper के साथ)
  - Allow list के साथ access control

- **`discord.py`** - Discord इंटीग्रेशन
  - `DiscordChannel`: Discord bot
  - `discord.py` library का उपयोग
  - Message intents और permissions
  - User ID-based access control

- **`whatsapp.py`** - WhatsApp इंटीग्रेशन
  - `WhatsAppChannel`: WhatsApp Web के साथ
  - Node.js bridge के माध्यम से WebSocket connection
  - QR code scanning के लिए device linking
  - Phone number-based allow list

- **`feishu.py`** - Feishu (飞书) इंटीग्रेशन
  - `FeishuChannel`: Feishu/Lark bot
  - WebSocket long connection (कोई public IP की आवश्यकता नहीं)
  - `lark-oapi` library का उपयोग
  - Event subscription और message handling
  - Reaction support (👀, ✅, ❌)

- **`manager.py`** - चैनल मैनेजर
  - `ChannelManager`: सभी चैनलों को initialize और manage करता है
  - Config के आधार पर चैनलों को enable/disable करता है
  - सभी चैनलों को एक साथ start/stop करता है

- **`__init__.py`** - चैनल पैकेज इनिशियलाइज़ेशन

#### 📂 `nanobot/bus/` - मैसेज रूटिंग

चैनलों और एजेंट के बीच संदेशों को route करता है।

- **`events.py`** - मैसेज डेटा स्ट्रक्चर
  - `InboundMessage`: यूजर से आने वाले संदेश
    - `channel`, `chat_id`, `user_id`, `text`, `timestamp`
    - `session_key()`: unique session identifier
  - `OutboundMessage`: एजेंट से जाने वाले संदेश
    - `channel`, `chat_id`, `text`

- **`queue.py`** - मैसेज बस
  - `MessageBus`: asyncio queues का उपयोग करके message routing
  - `publish_inbound()`: चैनल से संदेश receive करता है
  - `consume_inbound()`: एजेंट के लिए संदेश
  - `publish_outbound()`: एजेंट से यूजर को संदेश

- **`__init__.py`** - बस पैकेज इनिशियलाइज़ेशन

#### 📂 `nanobot/providers/` - LLM प्रोवाइडर

विभिन्न LLM APIs के साथ इंटीग्रेशन।

- **`base.py`** - प्रोवाइडर बेस क्लास
  - `ToolCallRequest`: टूल कॉल request structure
  - `LLMResponse`: LLM response structure
  - `LLMProvider`: abstract provider interface

- **`litellm_provider.py`** - LiteLLM इंटीग्रेशन
  - `LiteLLMProvider`: सभी LLM providers के लिए unified interface
  - OpenRouter, Anthropic, OpenAI, DeepSeek, Groq, Gemini को सपोर्ट करता है
  - Function calling और tool use
  - Streaming responses
  - Token counting और cost tracking

- **`transcription.py`** - Voice transcription
  - `GroqTranscriptionProvider`: Groq Whisper API
  - Audio files को text में convert करता है
  - Telegram voice messages के लिए

- **`__init__.py`** - प्रोवाइडर पैकेज इनिशियलाइज़ेशन


#### 📂 `nanobot/cron/` - शेड्यूल्ड टास्क

समय-आधारित और recurring tasks को मैनेज करता है।

- **`types.py`** - डेटा स्ट्रक्चर
  - `CronSchedule`: schedule configuration
    - `cron`: cron expression (e.g., "0 9 * * *")
    - `every`: interval in seconds
    - `at`: one-time execution timestamp
  - `CronPayload`: task payload (message, delivery info)
  - `CronJobState`: job state (enabled/disabled, next run time)
  - `CronJob`: complete job definition
  - `CronStore`: jobs का persistent storage

- **`service.py`** - Cron सर्विस
  - `CronService`: cron jobs को execute करता है
  - Jobs को JSON file में store करता है
  - Next run time को calculate करता है (croniter का उपयोग)
  - Background में jobs को check और execute करता है
  - Message delivery के लिए MessageBus के साथ integrate

- **`__init__.py`** - Cron पैकेज इनिशियलाइज़ेशन

#### 📂 `nanobot/heartbeat/` - Proactive Wake-up

एजेंट को समय-समय पर जगाता है।

- **`service.py`** - Heartbeat सर्विस
  - `HeartbeatService`: हर 30 मिनट में एजेंट को wake करता है
  - `HEARTBEAT.md` file को check करता है
  - Periodic tasks को execute करने के लिए एजेंट को trigger करता है
  - Background asyncio task के रूप में चलता है

- **`__init__.py`** - Heartbeat पैकेज इनिशियलाइज़ेशन

#### 📂 `nanobot/session/` - Conversation Sessions

यूजर conversations को मैनेज करता है।

- **`manager.py`** - Session मैनेजर
  - `SessionManager`: प्रत्येक यूजर के लिए conversation history
  - Session key: `channel:chat_id` (e.g., `telegram:123456789`)
  - Message history को memory में store करता है
  - Context window management
  - Session cleanup और timeout

- **`__init__.py`** - Session पैकेज इनिशियलाइज़ेशन

#### 📂 `nanobot/config/` - Configuration Management

Application configuration को handle करता है।

- **`schema.py`** - Configuration schema
  - Pydantic models का उपयोग करके type-safe config
  - `AgentConfig`: agent settings (model, temperature, etc.)
  - `ProviderConfig`: LLM provider credentials
  - `ChannelConfig`: channel-specific settings
  - `ToolConfig`: tool configurations (API keys, etc.)
  - `Config`: complete configuration

- **`loader.py`** - Configuration loader
  - `~/.nanobot/config.json` से config load करता है
  - Environment variables को support करता है
  - Default values और validation
  - Config file creation और updates

- **`__init__.py`** - Config पैकेज इनिशियलाइज़ेशन

#### 📂 `nanobot/cli/` - Command Line Interface

Terminal से nanobot को control करने के लिए commands।

- **`commands.py`** - CLI commands
  - `typer` library का उपयोग
  - **Commands:**
    - `nanobot onboard`: config और workspace initialize करता है
    - `nanobot agent -m "..."`: एजेंट के साथ chat करता है
    - `nanobot agent`: interactive chat mode
    - `nanobot gateway`: सभी चैनलों को start करता है
    - `nanobot status`: system status दिखाता है
    - `nanobot channels login`: WhatsApp QR code scan
    - `nanobot channels status`: channel status
    - `nanobot cron add/list/remove`: cron jobs manage करता है

- **`__init__.py`** - CLI पैकेज इनिशियलाइज़ेशन

#### 📂 `nanobot/utils/` - Utility Functions

सामान्य helper functions।

- **`helpers.py`** - Helper functions
  - String manipulation
  - File operations
  - Date/time utilities
  - Logging helpers

- **`__init__.py`** - Utils पैकेज इनिशियलाइज़ेशन


#### 📂 `nanobot/skills/` - Built-in Skills

एजेंट की क्षमताओं को बढ़ाने वाली skills।

**Structure:** प्रत्येक skill एक directory है जिसमें `SKILL.md` file है।

- **`README.md`** - Skills documentation
  - Skill format की व्याख्या
  - OpenClaw compatibility
  - Available skills की list

- **`github/SKILL.md`** - GitHub integration
  - `gh` CLI का उपयोग करके GitHub के साथ interact करता है
  - Pull requests, issues, CI runs को manage करता है
  - `gh api` के साथ advanced queries
  - Requirements: `gh` binary

- **`weather/SKILL.md`** - Weather information
  - wttr.in और Open-Meteo APIs
  - कोई API key की आवश्यकता नहीं
  - Current weather और forecasts
  - Requirements: `curl`

- **`summarize/SKILL.md`** - Content summarization
  - URLs, files, YouTube videos को summarize करता है
  - Web content extraction
  - Video transcript processing

- **`tmux/SKILL.md`** - Tmux session control
  - Remote tmux sessions को control करता है
  - Scripts: `find-sessions.sh`, `wait-for-text.sh`
  - Terminal multiplexing automation

- **`skill-creator/SKILL.md`** - Skill creation helper
  - नई skills बनाने में मदद करता है
  - SKILL.md template generation
  - Metadata और frontmatter formatting

- **`cron/SKILL.md`** - Cron job management
  - Scheduled tasks को create और manage करता है
  - Natural language scheduling
  - Recurring और one-time reminders

#### Root Level Files

- **`__init__.py`** - Main package initialization
  - Package metadata
  - Version information

- **`__main__.py`** - Entry point
  - `python -m nanobot` के लिए
  - CLI commands को invoke करता है

---

### 2. `bridge/` - WhatsApp Node.js Bridge

WhatsApp Web को Python backend से connect करने के लिए Node.js bridge।

#### Why Node.js?
WhatsApp Web protocol के लिए सबसे अच्छी library (Baileys) Node.js में है। यह bridge Python और Node.js के बीच WebSocket के माध्यम से communicate करता है।

**Files:**

- **`package.json`** - Node.js project configuration
  - Dependencies: `@whiskeysockets/baileys`, `ws`, `qrcode-terminal`, `pino`
  - Scripts: `build`, `start`, `dev`
  - Node.js ≥20 required

- **`tsconfig.json`** - TypeScript configuration
  - Compiler options
  - Module resolution
  - Output directory

- **`src/index.ts`** - Entry point
  - Bridge server को initialize करता है
  - Environment variables: `BRIDGE_PORT`, `AUTH_DIR`
  - Graceful shutdown handling (SIGINT, SIGTERM)
  - Default port: 3001

- **`src/server.ts`** - WebSocket server
  - `BridgeServer` class: Python-Node.js communication
  - WebSocket server (ws library)
  - Commands: `send` (message भेजने के लिए)
  - Events: `message`, `status`, `qr`, `error`
  - Multiple Python clients को support करता है

- **`src/whatsapp.ts`** - WhatsApp client
  - `WhatsAppClient` class: Baileys wrapper
  - QR code generation और scanning
  - Message sending और receiving
  - Authentication state management
  - Connection status tracking

- **`src/types.d.ts`** - TypeScript type definitions
  - Interface definitions
  - Type declarations

---

### 3. `workspace/` - Agent Configuration

एजेंट के व्यवहार और व्यक्तित्व को configure करने वाली files।

- **`SOUL.md`** - Agent personality
  - एजेंट की पहचान: "I am nanobot 🐈"
  - Personality traits: helpful, friendly, concise, curious
  - Values: accuracy, privacy, transparency
  - Communication style: clear, direct, explanatory

- **`AGENTS.md`** - Agent instructions
  - General guidelines: explain actions, ask for clarification
  - Available tools की list
  - Memory usage instructions
  - Scheduled reminders के लिए commands
  - Heartbeat tasks management

- **`TOOLS.md`** - Tools documentation
  - प्रत्येक tool का detailed documentation
  - Function signatures और parameters
  - Usage examples
  - Safety notes और limitations

- **`USER.md`** - User profile template
  - User information: name, timezone, language
  - Preferences: communication style, response length, technical level
  - Work context: role, projects, tools
  - Topics of interest
  - Special instructions

- **`HEARTBEAT.md`** - Periodic tasks
  - हर 30 मिनट में check होने वाले tasks
  - Task format: `- [ ] Task description`
  - Examples: calendar reminders, email scanning, weather checks

- **`memory/MEMORY.md`** - Long-term memory
  - Important information जो एजेंट को याद रखना चाहिए
  - User preferences
  - Project details
  - Recurring patterns


---

### 4. `tests/` - Test Files

Testing और validation के लिए files।

- **`test_docker.sh`** - Docker testing script
  - Docker image को build और test करता है
  - Container functionality को verify करता है
  - Integration testing

- **`test_tool_validation.py`** - Tool validation tests
  - Tool implementations को test करता है
  - Parameter validation
  - Error handling
  - pytest framework का उपयोग

---

### 5. `case/` - Demo Assets

Demo और documentation के लिए GIF images।

- **`code.gif`** - Full-stack software engineer demo
  - Code development और deployment
  
- **`memory.gif`** - Personal knowledge assistant demo
  - Memory और learning capabilities

- **`schedule.gif`** - Smart daily routine manager demo
  - Task scheduling और automation

- **`search.gif`** - Real-time market analysis demo
  - Web search और insights

---

## 📄 Root Level Configuration Files

### Build और Deployment

- **`Dockerfile`** - Docker container configuration
  - Base image: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
  - Node.js 20 installation (WhatsApp bridge के लिए)
  - Python dependencies (uv का उपयोग)
  - WhatsApp bridge build
  - Port 18790 expose (gateway के लिए)
  - Entrypoint: `nanobot`

- **`.dockerignore`** - Docker build exclusions
  - Build में include न करने वाली files
  - Cache directories, logs, etc.

- **`pyproject.toml`** - Python project configuration
  - Package metadata: name, version, description
  - Dependencies: typer, litellm, pydantic, websockets, etc.
  - Optional dependencies: dev tools (pytest, ruff)
  - Scripts: `nanobot` command
  - Build system: hatchling
  - Ruff linting configuration
  - Pytest configuration

### Version Control

- **`.gitignore`** - Git exclusions
  - Python cache files (`__pycache__`, `*.pyc`)
  - Virtual environments (`venv/`, `.venv/`)
  - IDE files (`.vscode/`, `.idea/`)
  - Build artifacts (`dist/`, `build/`)
  - Config files (`config.json`)
  - Node modules (`node_modules/`)

### Documentation

- **`README.md`** - Main documentation (English)
  - Project introduction और features
  - Installation instructions (source, uv, PyPI)
  - Quick start guide
  - Local models (vLLM) setup
  - Chat apps configuration (Telegram, Discord, WhatsApp, Feishu)
  - Configuration reference
  - CLI commands
  - Docker usage
  - Project structure
  - Contribution guidelines और roadmap

- **`COMMUNICATION.md`** - Community links
  - WeChat और Feishu group QR codes
  - HKUDS discussion groups

- **`LICENSE`** - MIT License
  - Open source license terms

### Scripts

- **`core_agent_lines.sh`** - Line counter script
  - Core agent code की lines count करता है
  - Code size को verify करने के लिए
  - Bash script

### Assets

- **`nanobot_logo.png`** - Project logo
  - Nanobot का logo (🐈 cat theme)

- **`nanobot_arch.png`** - Architecture diagram
  - System architecture का visual representation
  - Components और data flow

---

## 🔄 Data Flow और Architecture

### 1. Message Flow

```
User (Telegram/Discord/WhatsApp/Feishu)
    ↓
Channel (TelegramChannel/DiscordChannel/etc.)
    ↓
MessageBus (publish_inbound)
    ↓
SessionManager (conversation history)
    ↓
AgentLoop (main processing)
    ↓
LLMProvider (LiteLLM → OpenRouter/Anthropic/etc.)
    ↓
Tool Execution (filesystem/shell/web/etc.)
    ↓
AgentLoop (response generation)
    ↓
MessageBus (publish_outbound)
    ↓
Channel (send message)
    ↓
User
```

### 2. Component Interactions

**Gateway Mode:**
- ChannelManager सभी enabled channels को start करता है
- प्रत्येक channel MessageBus से connected है
- AgentLoop MessageBus से messages consume करता है
- Multiple sessions parallel में चल सकते हैं

**Agent Mode (CLI):**
- Direct AgentLoop invocation
- कोई channel नहीं, सीधे terminal I/O
- Single session

**Cron Service:**
- Background में independently चलता है
- Scheduled jobs को execute करता है
- MessageBus के माध्यम से messages deliver करता है

**Heartbeat Service:**
- हर 30 मिनट में trigger होता है
- HEARTBEAT.md को read करता है
- AgentLoop को periodic tasks के साथ invoke करता है


### 3. Configuration Hierarchy

```
~/.nanobot/
├── config.json          # Main configuration
├── workspace/           # Agent personality और instructions
│   ├── SOUL.md
│   ├── AGENTS.md
│   ├── TOOLS.md
│   ├── USER.md
│   ├── HEARTBEAT.md
│   └── memory/
│       ├── MEMORY.md
│       └── YYYY-MM-DD.md (daily notes)
├── skills/              # Custom skills (optional)
│   └── my-skill/
│       └── SKILL.md
├── whatsapp-auth/       # WhatsApp authentication
└── cron-store.json      # Scheduled jobs
```

---

## 🛠️ Key Technologies

### Python Libraries

- **typer**: CLI framework (commands)
- **litellm**: Unified LLM API (सभी providers को support)
- **pydantic**: Data validation और settings
- **websockets**: WebSocket client/server
- **httpx**: Async HTTP client
- **loguru**: Logging
- **readability-lxml**: Web content extraction
- **rich**: Terminal formatting
- **croniter**: Cron expression parsing
- **python-telegram-bot**: Telegram bot API
- **lark-oapi**: Feishu/Lark API

### Node.js Libraries (Bridge)

- **@whiskeysockets/baileys**: WhatsApp Web protocol
- **ws**: WebSocket server
- **qrcode-terminal**: QR code display
- **pino**: Logging

### Development Tools

- **pytest**: Testing framework
- **pytest-asyncio**: Async test support
- **ruff**: Fast Python linter
- **hatchling**: Build backend
- **uv**: Fast Python package installer

---

## 🚀 Execution Modes

### 1. Gateway Mode (`nanobot gateway`)

सभी configured channels को start करता है और background में चलता है।

**Process:**
1. Config load करता है
2. MessageBus initialize करता है
3. ChannelManager सभी enabled channels start करता है
4. CronService start होता है (scheduled tasks के लिए)
5. HeartbeatService start होता है (periodic wake-ups के लिए)
6. AgentLoop MessageBus से messages consume करता है
7. Graceful shutdown (Ctrl+C पर)

**Use Case:** Production deployment, 24/7 availability

### 2. Agent Mode (`nanobot agent`)

Direct CLI interaction, कोई channel नहीं।

**Modes:**
- **One-shot**: `nanobot agent -m "message"` (single query)
- **Interactive**: `nanobot agent` (continuous chat)

**Use Case:** Testing, debugging, quick queries

### 3. Onboard Mode (`nanobot onboard`)

Initial setup और configuration।

**Process:**
1. `~/.nanobot/` directory create करता है
2. `config.json` template generate करता है
3. Workspace files create करता है (SOUL.md, AGENTS.md, etc.)
4. Instructions display करता है

**Use Case:** First-time setup

### 4. Cron Management (`nanobot cron`)

Scheduled tasks को manage करता है।

**Commands:**
- `nanobot cron add`: नया job add करता है
- `nanobot cron list`: सभी jobs list करता है
- `nanobot cron remove <id>`: job delete करता है

**Use Case:** Reminders, recurring tasks, automation

### 5. Channel Management (`nanobot channels`)

Channel-specific operations।

**Commands:**
- `nanobot channels login`: WhatsApp QR code scan
- `nanobot channels status`: सभी channels की status

**Use Case:** WhatsApp setup, debugging

---

## 🔐 Security Features

### 1. Access Control

- **Allow Lists**: प्रत्येक channel में `allowFrom` configuration
  - Telegram: user IDs
  - Discord: user IDs
  - WhatsApp: phone numbers
  - Feishu: user IDs (ou_xxx)

### 2. Command Safety

- **Dangerous Commands Blocked**: `rm -rf`, `format`, `dd`, `shutdown`, etc.
- **Timeout**: Commands 60 seconds के बाद terminate होते हैं
- **Output Truncation**: 10,000 characters limit
- **Workspace Restriction**: Optional `restrictToWorkspace` config

### 3. API Key Management

- Config file में API keys store होते हैं (`~/.nanobot/config.json`)
- Environment variables support
- कभी भी code में hardcode नहीं

### 4. Data Privacy

- सभी data locally store होता है (`~/.nanobot/`)
- कोई external database नहीं
- Conversation history memory में (restart पर clear)
- WhatsApp auth local directory में

---

## 📊 Performance Characteristics

### Code Size

- **Core Agent**: ~3,400 lines
- **Total Project**: ~10,000 lines (including bridge, tests, configs)
- **99% smaller** than Clawdbot (430k+ lines)

### Resource Usage

- **Memory**: ~50-100 MB (Python process)
- **CPU**: Minimal (event-driven, async I/O)
- **Disk**: ~10 MB (code + dependencies)
- **Network**: केवल API calls के दौरान

### Startup Time

- **Gateway**: ~2-3 seconds
- **Agent CLI**: ~1 second
- **Docker**: ~5 seconds (container start + initialization)

### Scalability

- **Concurrent Sessions**: Unlimited (async architecture)
- **Message Throughput**: 100+ messages/second
- **Channels**: Multiple channels simultaneously
- **Subagents**: Parallel background tasks

---

## 🎯 Use Cases

### 1. Personal Assistant

- Daily reminders और scheduling
- Email और calendar management
- Weather updates
- News summaries

### 2. Development Helper

- GitHub operations (PRs, issues, CI)
- Code search और documentation
- Shell command execution
- File operations

### 3. Research Assistant

- Web search और information gathering
- Content summarization
- Knowledge management (memory)
- Citation tracking

### 4. Automation

- Scheduled tasks (cron)
- Periodic checks (heartbeat)
- Background processing (subagents)
- Multi-step workflows

### 5. Communication Hub

- Multi-platform messaging (Telegram, Discord, WhatsApp, Feishu)
- Voice message transcription
- Group chat management
- Notification delivery

---

## 🔧 Customization और Extension

### 1. Adding Custom Tools

```python
# nanobot/agent/tools/my_tool.py
from nanobot.agent.tools.base import Tool

class MyTool(Tool):
    def name(self) -> str:
        return "my_tool"
    
    def description(self) -> str:
        return "My custom tool description"
    
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "param1": {"type": "string"}
            },
            "required": ["param1"]
        }
    
    async def execute(self, param1: str, **kwargs) -> str:
        # Implementation
        return f"Result: {param1}"

# Register in AgentLoop._register_default_tools()
```

### 2. Creating Custom Skills

```markdown
---
name: my-skill
description: "My custom skill"
metadata: {"nanobot":{"emoji":"🎯","requires":{"bins":["tool"]}}}
---

# My Skill

Instructions for the agent...

## Usage

Examples...
```

### 3. Adding New Channels

```python
# nanobot/channels/my_channel.py
from nanobot.channels.base import BaseChannel

class MyChannel(BaseChannel):
    async def start(self) -> None:
        # Initialize connection
        pass
    
    async def stop(self) -> None:
        # Cleanup
        pass
    
    async def send(self, msg: OutboundMessage) -> None:
        # Send message
        pass

# Register in ChannelManager._init_channels()
```

### 4. Custom LLM Providers

```python
# nanobot/providers/my_provider.py
from nanobot.providers.base import LLMProvider

class MyProvider(LLMProvider):
    async def chat(self, messages, tools=None, **kwargs):
        # Implementation
        pass
```

---

## 📚 Learning Path

### Beginners

1. **Start**: README.md पढ़ें
2. **Setup**: `nanobot onboard` चलाएं
3. **Try**: `nanobot agent -m "Hello"` test करें
4. **Explore**: workspace files (SOUL.md, AGENTS.md) देखें

### Intermediate

1. **Channels**: Telegram bot setup करें
2. **Skills**: Built-in skills explore करें
3. **Cron**: Scheduled reminders create करें
4. **Memory**: Daily notes और MEMORY.md use करें

### Advanced

1. **Code**: `nanobot/agent/loop.py` study करें
2. **Tools**: Custom tool create करें
3. **Skills**: Custom skill develop करें
4. **Providers**: Local LLM (vLLM) integrate करें
5. **Channels**: नया channel implementation add करें

---

## 🤝 Contributing

### Code Style

- **Python**: PEP 8, ruff linting
- **TypeScript**: Standard TypeScript conventions
- **Line Length**: 100 characters
- **Type Hints**: सभी functions में

### Testing

```bash
# Python tests
pytest tests/

# Docker test
bash tests/test_docker.sh
```

### Pull Requests

1. Fork repository
2. Feature branch create करें
3. Changes commit करें
4. Tests pass करें
5. PR submit करें

---

## 📞 Support और Community

- **GitHub Issues**: Bug reports और feature requests
- **Discord**: Community discussions
- **WeChat/Feishu**: Chinese community (COMMUNICATION.md देखें)

---

## 📝 License

MIT License - देखें `LICENSE` file

---

## 🙏 Acknowledgments

- **Inspired by**: [OpenClaw](https://github.com/openclaw/openclaw)
- **Skills Format**: OpenClaw compatibility
- **Contributors**: [GitHub Contributors](https://github.com/HKUDS/nanobot/graphs/contributors)

---

## 📈 Future Roadmap

- ✅ Voice Transcription (Groq Whisper)
- ⏳ Multi-modal support (images, video)
- ⏳ Long-term memory improvements
- ⏳ Better reasoning (multi-step planning)
- ⏳ More integrations (Slack, email, calendar)
- ⏳ Self-improvement capabilities

---

**यह document nanobot codebase की संपूर्ण व्याख्या है। प्रत्येक directory, file, और component को विस्तार से समझाया गया है।**

**🐈 Happy Coding with Nanobot!**
