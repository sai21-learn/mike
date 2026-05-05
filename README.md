<p align="center">
  <img src="assets/banner.png" alt="Mike" />
</p>

<p align="center">
  A local-first personal AI assistant powered by Ollama.<br>
  Multi-provider support, 35+ tools, multimodal generation, intent-based routing, persistent memory, RAG, and voice I/O.
</p>

## Features

- **Multi-Provider Support**: Ollama (local), Ollama Cloud (remote), Chutes AI (comprehensive cloud platform)
- **35+ Built-in Tools**: Web search, git operations, file ops, weather, gold prices, task management, multi-model analysis, and more
- **Intent Classification**: LLM-based smart routing with heuristic fallback - automatically detects what you need
- **Reasoning Levels**: Fast / Balanced / Deep - auto-detected per query or user-controlled
- **Multimodal Generation**: Generate images (FLUX.1), videos (Wan2.1), and music (DiffRhythm) via Chutes AI
- **Vision Analysis**: Analyze images using local Ollama vision models or Chutes cloud
- **Knowledge Base (RAG)**: Feed your own documents (PDF, TXT, MD) with cross-encoder reranking for accurate retrieval
- **Tool Timeline UI**: Visual execution steps showing tool calls, duration, and results
- **Thinking Blocks**: Collapsible reasoning visualization for thinking models (DeepSeek-R1, QwQ, etc.)
- **Chat History**: Claude-style conversation sidebar with search, edit, and auto-titles
- **Parallel Tool Execution**: Async tool executor runs multiple tools concurrently with live progress streaming
- **Dynamic Tool Selection**: Intent-based scoring sends only 3-8 relevant tools per query instead of all 30+
- **Multi-Agent Orchestrator**: Decomposes complex tasks into parallel subtasks handled by independent sub-agents
- **Document Processing**: Intelligent chunking pipeline for PDF, DOCX, XLSX with RAG retrieval for large files
- **Dynamic Context Budgets**: Proportional token allocation that adapts to any model size (4K to 1M+)
- **Semantic History**: ChromaDB-backed retrieval of relevant past messages, not just recent ones
- **Context Management**: Auto-compaction with LLM-powered summarization and context window tracking
- **Fact Extraction**: Automatically learns facts about you from conversations
- **Memory System**: Persistent SQLite storage with working memory and auto-compaction
- **Personas**: Switch between assistant modes (default, coder, researcher, creative, planner)
- **Dynamic Skills**: Create new tools at runtime - Mike can build its own skills
- **Multi-Model Analysis**: Run queries through multiple AI models simultaneously and combine insights
- **Web UI**: Modern dark glass-card interface with real-time WebSocket communication
- **Light & Dark Mode**: Theme toggle with localStorage persistence and OS preference detection
- **Stop Generation**: Interrupt any response mid-stream and immediately send a new prompt
- **Voice Mode**: Full-screen voice overlay with waveform visualizer, real-time transcript, and interrupt controls
- **Floating Mobile Orb**: Iron Man arc reactor style FAB for quick voice access on mobile
- **Draggable Camera**: Resizable, draggable camera preview with edge snapping and position persistence
- **Voice Input/Output**: Speech-to-text (Whisper/Chutes), text-to-speech (Browser/Edge/ElevenLabs/Kokoro)
- **Strong Identity System**: Stays in character regardless of underlying model, per-user personalization
- **Telegram Bot**: Full-featured Telegram integration with 20+ commands
- **Authentication**: Optional email/password login with session management, CLI user management
- **Project Context**: Auto-detects project type and loads MIKE.md/CLAUDE.md instructions

## Requirements

- **Python 3.10 to 3.13+** (Fully tested on 3.13)
- [Ollama](https://ollama.ai) installed and running
- [uv](https://github.com/astral-sh/uv) (Highly recommended for 10x faster installation)
- **Node.js 18+** (Required for Web UI)
- 16GB RAM recommended

```bash
# Verify your version
python3 --version
```

## Installation

### Quick Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/sai21-learn/mike/main/install.sh | bash
```

> **Note:** The script automatically detects `uv` for a faster setup. If not found, it falls back to standard `pip/venv`.

### Manual Installation (If Quick Install Fails)

If you prefer `uv` (recommended):

```bash
# 1. Clone and setup
git clone https://github.com/sai21-learn/mike.git ~/.mike
cd ~/.mike/src

# 2. Create environment and install
uv venv ../venv --python 3.13
source ../venv/bin/activate
uv pip install -e ".[all]"

# 3. Use Mike!
mike --version
```

### Using pip

```bash
# Basic installation
pip install mike-ai-assistant

# With UI support
pip install mike-ai-assistant[ui]

# With voice support
pip install mike-ai-assistant[voice]

# Everything
pip install mike-ai-assistant[all]
```

### From Source

```bash
git clone https://github.com/sai21-learn/mike.git
cd mike
python3.12 -m venv venv
source venv/bin/activate
pip install -e ".[ui]"
pip install python-multipart
```

### Install Ollama Models

```bash
# Required for chat
ollama pull qwen2.5:3b        # Fast & capable
ollama pull llama3.2          # Modern small model

# Required for RAG (knowledge base)
ollama pull nomic-embed-text  # Text embeddings

# Optional
ollama pull deepseek-v2.5     # Advanced reasoning
ollama pull llava             # Image understanding (vision)
ollama pull llama3.2-vision   # Better vision model
```

### Web UI Setup (Additional Steps)

The Web UI requires Node.js. If `mike --dev` shows `vite: command not found`:

```bash
# 1. Install Node.js (macOS)
brew install node

# 2. Install frontend dependencies
cd ~/.mike/web
npm install

# 3. Now run the dev server
mike --dev
```

## Usage

### CLI Mode (Default)

```bash
mike                 # Interactive mode
mike --fast          # Use fast reasoning level
mike --deep          # Use deep reasoning level
mike --level balanced  # Explicit reasoning level
```

### Web UI

```bash
mike --dev
# Opens at http://localhost:7777 (backend) and http://localhost:3000 (frontend)
```

### Voice Mode

```bash
mike --voice
# Requires: pip install mike-ai-assistant[voice]
```

### Single Query

```bash
mike chat "What's the weather in London?"
mike chat "Explain recursion" --deep
mike chat "What time is it?" --fast
```

### Telegram Bot

Full-featured Telegram integration with all capabilities:

```bash
# Interactive setup wizard
mike telegram setup

# Or manual setup:
mike config set telegram bot_token YOUR_BOT_TOKEN
mike telegram webhook https://your-domain.com  # Set webhook (recommended)

# Now just run your server - Telegram works automatically!
mike --dev
```

**Telegram Commands:**

| Command | Description |
|---------|-------------|
| `/help` | Show all commands |
| `/model` | Show/switch AI model |
| `/models` | List available models |
| `/provider` | Show/switch provider |
| `/clear` | Clear conversation |
| `/mode <fast\|balanced\|deep>` | Set reasoning mode |
| `/search <query>` | Web search |
| `/knowledge <query>` | Search knowledge base |
| `/remember <fact>` | Save a fact about you |
| `/status` | System status |
| `/weather` | Current weather |
| `/name <new name>` | Change assistant name |

Plus all regular chat capabilities - web search, tool execution, RAG, etc.

### Other Commands

```bash
mike --help      # Show all options
mike setup       # Run setup wizard
mike models      # List Ollama models
mike personas    # List personas
mike --daemon    # Run as background daemon

# User management (when auth enabled)
mike user create     # Create user account
mike user list       # List users
mike user passwd     # Reset password
mike user rename     # Change display name
mike user email      # Change email
mike user delete     # Delete user
```

## Web UI Features

The web UI (`mike --dev`) includes:

- **Dark Glass UI**: Glass-card design with backdrop blur, iridescent orb, and gradient accents
- **Light & Dark Mode**: One-click theme toggle, persists across sessions, respects OS preference
- **Voice Overlay**: Full-screen voice mode with XL orb, real-time waveform visualizer, live transcript display
- **Stop Generation**: Click the stop button (or interrupt via voice) to halt any response mid-stream
- **Floating Mobile Orb**: Arc reactor style floating action button for quick voice access on mobile
- **Draggable Camera**: Resizable camera preview with drag-to-move, edge snapping, and localStorage persistence
- **Empty State**: Welcome greeting with quick action cards (Start Conversation, Generate Image, Web Search, Write Code)
- **Chat Bubbles**: Right-aligned user messages (cyan accent), left-aligned assistant messages (glass-card)
- **Unified Smart Mode**: Auto-detects when to use fast chat vs full agent mode based on intent classification
- **Reasoning Level Selector**: Fast (Zap) / Auto (Scale) / Deep (Brain) controls
- **Tool Timeline**: Expandable panel showing each tool call, arguments, duration, and results
- **Thinking Blocks**: Collapsible purple blocks showing model reasoning (for thinking models)
- **Context Window Tracker**: Color-coded bar (blue < 60%, yellow 60-80%, red > 80%) showing token usage
- **Media Generation**: Generate and preview images, videos, and audio inline
- **File Attachments**: Drag-and-drop upload for vision analysis
- **Provider Switching**: Change LLM provider and model on the fly
- **Voice Input/Output**: Push-to-talk with multiple TTS/STT providers
- **Dashboard Widgets**: Weather, time, system status, quick commands, voice control
- **Settings Panel**: Provider configuration, voice settings, memory management, system instructions editor
- **Animated Orb**: Iridescent glass shader with volume-reactive sizing for idle/listening/speaking/thinking states

## CLI Commands

Inside the interactive CLI:

| Command | Description |
|---------|-------------|
| `/help` | Show help |
| `/models` | List available models |
| `/model <name>` | Switch to a different model |
| `/provider <name>` | Switch provider (ollama, ollama_cloud, chutes) |
| `/persona <name>` | Switch persona |
| `/personas` | List personas |
| `/tools` | List available tools |
| `/facts` | Show stored facts |
| `/memory` | Show working memory |
| `/context` | Show context window stats |
| `/level` | Show/set reasoning level |
| `/clear` | Clear conversation |
| `/cls` | Clear screen |
| `/init` | Create MIKE.md project config |
| `/history` | Show recent history |
| `/quit` | Exit |

## Architecture

### Intent Classification System

Mike uses an LLM-based intent classifier that replaces hardcoded keyword matching:

```
User Message → Intent Classifier → Route to appropriate handler
                    │
                    ├── Intent: CHAT, SEARCH, WEATHER, CODE, GIT, SHELL, ...
                    ├── Confidence: 0.0 - 1.0
                    ├── Reasoning Level: fast / balanced / deep
                    └── Suggested Tools: [web_search, get_weather, ...]
```

**17 Intent Types**: CHAT, SEARCH, WEATHER, TIME_DATE, FILE_OP, CODE, GIT, SHELL, CALCULATE, RECALL, CONTROL, VISION, IMAGE_GEN, VIDEO_GEN, MUSIC_GEN, NEWS, FINANCE

### Smart Auto-Tools

Mike automatically detects when to use tools without being asked:

- **Current events**: "Who is the president?" → auto web search
- **Prices**: "What's the gold price?" → auto GoldAPI lookup
- **Weather**: "Weather in London" → auto weather lookup
- **News**: "Latest tech news" → auto news search
- **Time**: "What time is it in Tokyo?" → auto time lookup
- **Images**: "Draw a sunset" → auto image generation
- **Vision**: Attach an image → auto vision analysis

Context-aware commands also work:
```
You: Tell me about the Mars mission
Mike: [answers from knowledge]
You: search the web
Mike: [searches for "Mars mission" using previous context]
```

### Provider System

```
┌─────────────────────────────────────────────────┐
│               BaseProvider (ABC)                  │
│  chat(), stream(), chat_with_tools(), vision()   │
│  discover_models(), get_model_for_task()         │
└──────────────┬────────────────┬─────────────────┘
               │                │
   ┌───────────┴──┐  ┌────────┴─────────┐  ┌───────────────┐
   │    Ollama     │  │   OllamaCloud    │  │    Chutes      │
   │  (local LLM)  │  │ (remote Ollama)  │  │ (cloud AI)     │
   │  Tools: native│  │ Tools: native    │  │ LLM+TTS+STT   │
   │  Vision: yes  │  │ Vision: yes      │  │ Image+Video    │
   └──────────────┘  └──────────────────┘  │ Music+Vision   │
                                            └───────────────┘
```

## Available Tools (35+)

### Web & Information
| Tool | Description |
|------|-------------|
| `web_search` | Search with DuckDuckGo (default) or Brave |
| `web_fetch` | Fetch and extract content from URLs |
| `get_current_news` | Get latest news on a topic |
| `get_weather` | Current weather (wttr.in or OpenWeatherMap) |
| `get_current_time` | Get time in any timezone |
| `get_gold_price` | Live gold/silver prices (GoldAPI.io) |

### File Operations
| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Write/create files |
| `edit_file` | Search and replace in files |
| `list_files` | List directory contents |
| `glob_files` | Find files by pattern (e.g., `**/*.py`) |
| `grep` | Search file contents with regex |
| `search_files` | Search for text in files |
| `get_project_structure` | Get directory tree |

### Git Operations
| Tool | Description |
|------|-------------|
| `git_status` | Show working tree status |
| `git_diff` | Show changes (staged/unstaged) |
| `git_log` | Show commit history |
| `git_add` | Stage files |
| `git_commit` | Create commits |
| `git_branch` | List/create/switch branches |
| `git_stash` | Stash changes |

### Multimodal Generation
| Tool | Description |
|------|-------------|
| `generate_image` | Generate images from text (FLUX.1-schnell via Chutes) |
| `generate_video` | Generate videos from text/image (Wan2.1 via Chutes) |
| `generate_music` | Generate music with optional lyrics (DiffRhythm via Chutes) |
| `analyze_image` | Analyze images (Ollama vision or Chutes) |
| `analyze_document` | Analyze document content |

### Task Management
| Tool | Description |
|------|-------------|
| `task_create` | Create a new task |
| `task_update` | Update task status |
| `task_list` | List all tasks |
| `task_get` | Get task details |

### Multi-Model Analysis
| Tool | Description |
|------|-------------|
| `multi_model_analyze` | Run query through multiple AI models simultaneously |
| `analyze_parallel` | Parallel analysis with different model types |

### Utilities
| Tool | Description |
|------|-------------|
| `calculate` | Math expressions |
| `run_command` | Run shell commands (with confirmation) |
| `save_memory` | Save information to memory |
| `recall_memory` | Search saved memories |
| `github_search` | Search GitHub repos/code |
| `create_skill` | Dynamically create new skills |

## Knowledge Base (RAG)

Mike includes a RAG (Retrieval Augmented Generation) system that lets you feed it your own documents. When you ask questions, Mike searches your knowledge base and uses relevant information to give accurate, personalized answers.

### How It Works

```
Your Question → Embed Query → Vector Search (20 candidates) → Cross-Encoder Rerank → Top 5 → Inject into Prompt → AI Answers
```

### Two-Stage Retrieval

1. **Stage 1 - Fast Retrieval**: Bi-encoder embeddings search ChromaDB/Qdrant for top 20 candidates
2. **Stage 2 - Accurate Reranking**: Cross-encoder (`ms-marco-MiniLM-L-6-v2`) scores each query-document pair for precise relevance

### Quick Start

```bash
# Install embedding model (required once)
ollama pull nomic-embed-text

# Add a document
mike knowledge add ~/Documents/my_resume.pdf

# Add a folder of documents
mike knowledge add ~/Documents/work/ --recursive

# Sync all configured sources
mike knowledge sync --personal
```

### Knowledge Commands

| Command | Description |
|---------|-------------|
| `mike knowledge add <file>` | Add a file (PDF, TXT, MD) |
| `mike knowledge add <dir> -r` | Add directory recursively |
| `mike knowledge list` | List all sources and chunk counts |
| `mike knowledge search <query>` | Test semantic search |
| `mike knowledge remove <source>` | Remove a source |
| `mike knowledge clear` | Clear entire knowledge base |
| `mike knowledge sync` | Sync docs/ folder |
| `mike knowledge sync --personal` | Also sync ~/.mike/knowledge/personal/ |
| `mike knowledge sync --projects` | Also sync project READMEs from ~/Developer/ |

### Personal Knowledge (Private)

Store personal information outside of git:

```bash
mkdir -p ~/.mike/knowledge/personal
cp ~/Documents/notes.md ~/.mike/knowledge/personal/
mike knowledge sync --personal
```

### Supported File Types

| Type | Extension | Notes |
|------|-----------|-------|
| Text | `.txt` | Plain text files |
| Markdown | `.md` | Documentation, notes |
| PDF | `.pdf` | Resumes, reports, books |

### Configuration

In `~/.mike/config/settings.yaml`:

```yaml
memory:
  vector_store: knowledge/chroma_db
  rerank: true
  rerank_model: "cross-encoder/ms-marco-MiniLM-L-6-v2"
  relevance_threshold: 0.5
  embedding_dim: 768

models:
  embeddings: nomic-embed-text
```

## Multi-Provider Support

Mike supports multiple LLM providers. Configure in `~/.mike/config/settings.yaml`:

```yaml
# Default provider
provider: ollama

# Provider-specific settings
providers:
  ollama:
    model: llama3.2
  ollama_cloud:
    base_url: https://your-ollama-server.com
    api_key: your_key
  chutes:
    api_key: ${CHUTES_API_KEY}
    models:
      default: "Qwen/Qwen3-32B"
      reasoning: "deepseek-ai/DeepSeek-V3"
      deep: "moonshotai/Kimi-K2.5-TEE"
      vision: "Qwen/Qwen2.5-VL-72B-Instruct"
      code: "Qwen/Qwen2.5-Coder-32B-Instruct"
      fast: "unsloth/gemma-3-4b-it"
```

Switch providers at runtime:
```bash
/provider ollama
/provider chutes
/provider ollama_cloud
```

## Configuration

Configuration is stored in `~/.mike/`:

```
~/.mike/
├── config/
│   ├── settings.yaml     # Main config (models, providers, integrations)
│   ├── rules.md          # Safety rules
│   └── personas/         # Persona definitions
├── memory/
│   ├── facts.md          # Learned facts about user
│   ├── entities.json     # Tracked entities
│   └── mike.db         # SQLite conversation history
├── knowledge/
│   ├── personal/         # Personal docs (outside git)
│   └── notes/            # Quick notes
├── skills/               # User-created custom skills
├── generated/            # Generated media files (auto-cleanup)
└── logs/                 # Application logs
```

### Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```bash
# LLM Providers (optional - for cloud models)
CHUTES_API_KEY=your_key        # Chutes AI (recommended for multimodal)

# Web Search (highly recommended)
BRAVE_API_KEY=your_key          # Brave Search - primary search provider
                                 # Get free key at: https://brave.com/search/api/

# APIs (optional)
GOLD_API_KEY=your_key           # GoldAPI.io - live gold/silver prices
OPENWEATHER_API_KEY=your_key    # Weather data
GITHUB_TOKEN=your_token         # GitHub integration

# Voice (optional)
ELEVEN_LABS_API_KEY=your_key    # ElevenLabs TTS

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your_token

# Authentication (optional)
MIKE_AUTH_ENABLED=false             # Enable login (manage users via: mike user create)

# Vector DB (optional - defaults to ChromaDB local)
QDRANT_URL=your_url             # Qdrant cloud URL
QDRANT_API_KEY=your_key         # Qdrant API key
```

## Customization

### Assistant Name

The assistant name is configurable (not hardcoded as "Mike"):

```bash
# Via Telegram
/name Aria

# Via settings.yaml
assistant:
  name: Aria
```

### Personas

- **default**: Balanced general assistant
- **coder**: Pair programming mode
- **researcher**: Information analysis
- **creative**: Brainstorming partner
- **planner**: Productivity coach

Switch with `/persona coder` or `mike persona coder`.

### Project Context

Mike auto-detects your project type and loads project-specific instructions:

```bash
# Create a MIKE.md in any project root
echo "Always use TypeScript. Prefer functional components." > MIKE.md

# Also supports: .mike/soul.md, .mike/instructions.md, CLAUDE.md
```

Detected project types: Python, Node.js, PHP/Laravel, Rust, Go

### Adding Custom Skills

Create `~/.mike/skills/my_skill.py`:

```python
def my_function(param: str) -> dict:
    """Do something useful."""
    return {"success": True, "result": "..."}
```

Or let Mike create them dynamically:
```
You: Create a skill that fetches stock prices
Mike: [creates ~/.mike/skills/fetch_stock_price.py]
```

## Authentication (Optional)

Mike supports optional email/password authentication with session-based login. User management is done entirely via CLI.

### Setup

```bash
# Install auth dependencies
pip install -e ".[auth]"

# Enable auth
export MIKE_AUTH_ENABLED=true
```

### User Management (CLI)

All user operations are handled through the command line:

```bash
# Create a user account
mike user create
mike user create -e user@example.com -p secret -n "John"

# List all users
mike user list

# Reset a user's password
mike user passwd user@example.com

# Change display name
mike user rename user@example.com -n "New Name"

# Change email address
mike user email old@example.com -e new@example.com

# Delete a user
mike user delete user@example.com
```

Users are created with email verified. No email/SMTP setup required.

## Troubleshooting

### Dependency conflicts

If you encounter installation issues, we recommend using `uv` which resolves conflicts much better than standard `pip`:

```bash
pip install uv
uv pip install -e ".[all]"
```

### `vite: command not found`

Node.js and frontend dependencies are missing:

```bash
brew install node
cd ~/.mike/web
npm install
```

### `python-multipart` error

```bash
source ~/.mike/venv/bin/activate
pip install python-multipart
```

### `mike: command not found`

```bash
# Option 1: Activate venv first
source ~/.mike/venv/bin/activate
mike

# Option 2: Add alias
echo 'alias mike="~/.mike/venv/bin/mike"' >> ~/.zshrc
source ~/.zshrc
```

### Backend starts but frontend doesn't load

Make sure both ports are accessible:
- Backend: http://localhost:7777
- Frontend: http://localhost:3000

Check that `npm install` completed successfully in `~/.mike/web`.

## Development

### Setup

```bash
git clone https://github.com/sai21-learn/mike.git
cd mike

# Python backend (use Python 3.10-3.12)
python3.12 -m venv venv
source venv/bin/activate
pip install -e ".[all]"
pip install python-multipart

# React frontend
cd web
npm install
cd ..
```

### Running in Dev Mode

```bash
mike --dev
# Backend at http://localhost:7777
# Frontend at http://localhost:3000 (with hot reload)
```

### Project Structure

```
mike/
├── mike/                  # Python backend (~6,000 lines)
│   ├── __init__.py          # Package init, version, data dirs
│   ├── assistant.py         # Main Mike class, ProjectContext
│   ├── cli.py               # Click CLI entry point
│   ├── core/                # Core engine
│   │   ├── agent.py         # Agentic loop with tool calling
│   │   ├── context_manager.py  # Context + auto-compaction + SQLite
│   │   ├── intent.py        # LLM-based intent classification
│   │   ├── router.py        # Tool routing (intent + keyword fallback)
│   │   ├── tools.py         # 35+ tool definitions + dynamic selection
│   │   ├── tool_executor.py # Async parallel tool execution engine
│   │   ├── orchestrator.py  # Multi-agent task decomposition
│   │   ├── sub_agent.py     # Lightweight sub-agent for subtasks
│   │   ├── fact_extractor.py  # Learns facts from conversations
│   │   └── ollama_client.py # Legacy Ollama client
│   ├── providers/           # LLM provider abstractions
│   │   ├── base.py          # BaseProvider, Message, ModelInfo
│   │   ├── ollama.py        # Local Ollama (tools, vision)
│   │   ├── ollama_cloud.py  # Remote Ollama server
│   │   └── chutes.py        # Chutes AI (LLM/TTS/STT/Image/Video/Music)
│   ├── skills/              # Tool implementations
│   │   ├── web_search.py    # DuckDuckGo/Brave search
│   │   ├── file_ops.py      # File operations
│   │   ├── shell.py         # Shell command execution
│   │   ├── weather.py       # Weather (wttr.in/OpenWeather)
│   │   ├── calculator.py    # Math calculations
│   │   ├── datetime_ops.py  # Time/date operations
│   │   ├── memory_ops.py    # Fact saving/retrieval
│   │   ├── github_ops.py    # GitHub integration
│   │   ├── notes.py         # Quick notes
│   │   ├── telegram.py      # Telegram messaging
│   │   ├── media_gen.py     # Image/video/music generation
│   │   ├── document_processor.py  # PDF/DOCX/XLSX chunking + RAG
│   │   ├── multi_model_analysis.py  # Multi-model parallel queries
│   │   └── skill_creator.py # Dynamic skill creation
│   ├── knowledge/           # RAG system
│   │   └── rag.py           # RAG engine (ChromaDB/Qdrant + reranking)
│   ├── integrations/        # External integrations
│   │   └── telegram_bot.py  # Full Telegram bot
│   ├── auth/                # Authentication system
│   │   ├── models.py        # SQLAlchemy ORM models (User, Session, Token)
│   │   ├── db.py            # Database operations
│   │   ├── email_auth.py    # Email/password login
│   │   ├── middleware.py    # Auth middleware, CSRF, security headers
│   │   ├── security.py      # Password hashing (argon2), tokens
│   │   ├── credentials.py   # Credential management
│   │   ├── claude.py        # Claude auth
│   │   └── codex.py         # Codex auth
│   ├── ui/                  # User interfaces
│   │   ├── app.py           # FastAPI WebSocket server
│   │   ├── terminal.py      # Rich terminal UI
│   │   └── diff.py          # Diff view
│   └── voice/               # Voice I/O
│       └── voice_mode.py    # Whisper STT + system TTS
├── web/                     # React frontend (~3,500 lines)
│   ├── src/
│   │   ├── App.tsx          # Main app (modes, settings, voice)
│   │   ├── components/
│   │   │   ├── chat/        # MessageBubble, MessageList, ThinkingBlock, ToolStatus, EmptyState
│   │   │   ├── input/       # UnifiedInput, FileUpload, FilePreview
│   │   │   ├── settings/    # SettingsPanel, SystemInstructions, MemoryPanel
│   │   │   ├── orb/         # Animated orb, FloatingOrb, OrbRings
│   │   │   ├── voice/       # VoiceOverlay, WaveformVisualizer
│   │   │   ├── camera/      # DraggableCamera
│   │   │   ├── sidebar/     # ChatSidebar, ChatItem, UserMenu
│   │   │   ├── auth/        # LoginPage, ProtectedRoute
│   │   │   ├── dashboard/   # DashboardView, WidgetCard
│   │   │   └── widgets/     # Weather, Time, Status, Voice, Commands
│   │   ├── contexts/        # AuthContext
│   │   ├── hooks/           # useWebSocket, useVoice, useFileUpload, useWakeWord, useCamera, useTheme, useDraggable
│   │   └── types/           # TypeScript interfaces
│   └── dist/                # Production build
├── config/                  # Default configuration templates
│   ├── settings.yaml        # Default settings
│   ├── rules.md             # Safety rules
│   └── personas/            # Persona definitions
└── docs/                    # Documentation
```

## License

MIT
