# 🚀 AI Landing Page Generator

> **Multi-agent system that generates production-ready, conversion-optimized HTML landing pages for any business type** — powered by Azure OpenAI (GPT-5 Mini), DALL-E 3, Pixabay, and Microsoft AutoGen.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Multi-Agent Pipeline** | 9 specialized AI agents collaborate through a 4-phase parallel pipeline |
| **30+ Business Verticals** | Industry-specific strategy, copy, and design for SaaS, Healthcare, E-commerce, Consulting, Events, and 25+ more |
| **Dual Theme Engine** | Light and Dark themes with glassmorphism, micro-animations, and 2025 design trends |
| **Smart Image Sourcing** | DALL-E 3 generation, Pixabay stock photos, user URLs, or combined fallback chains |
| **Post-Integration QA** | Review Agent inspects the *assembled HTML* (not just text descriptions) for bugs, accessibility, and brand alignment |
| **Interactive Editor** | Conversational editing loop — describe changes in plain English and the AI applies them |
| **Parallel Execution** | Phases 1 & 2 run agents concurrently for 2-3× faster generation |

---

## 🏗️ Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full component diagram and data flow.

See [WORKFLOW.md](WORKFLOW.md) for the 4-phase agent pipeline diagram.

---

## 📋 Prerequisites

- **Python 3.10+**
- **One LLM provider** (pick one):
  - **Groq** (recommended, free) — [console.groq.com](https://console.groq.com)
  - **Ollama** (local, free) — [ollama.com](https://ollama.com)
  - **Azure OpenAI** — org/paid access with a GPT deployment
- *(Optional)* Azure DALL-E 3 deployment for AI image generation
- *(Optional)* [Pixabay API key](https://pixabay.com/api/docs/) for stock photos (free)

---

## 🛠️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/landing-page-generator.git
cd landing-page-generator

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure credentials
copy .env.example .env       # Windows
# cp .env.example .env       # macOS / Linux
```

Open `.env` in your editor and fill in credentials. **Free option (Groq):**

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile

# Optional — free Pixabay key for hero images
PIXABAY_API_KEY=your-pixabay-key
```

**Local free option (Ollama):** install Ollama, run `ollama pull llama3.2`, then set `LLM_PROVIDER=ollama`.

See `.env.example` for Azure and optional DALL-E settings.

> ⚠️ **Never commit `.env`** — it is already listed in `.gitignore`.
---

## 🚀 Usage

```bash
python -m src.main
```

The interactive CLI will guide you through:

1. **Business info** — use the built-in sample (TechFlow Solutions) or enter your own
2. **Theme** — Light or Dark
3. **Image source** — DALL-E 3, Pixabay, both, your own URL, or none
4. **Generation** — the 4-phase pipeline runs (~2-3 minutes)
5. **Editing** — optionally make iterative changes via plain-English prompts

The generated HTML file is saved to `output/<business_name>/`.

---

## 📁 Project Structure

```
landing-page-generator/
├── README.md                  # This file
├── ARCHITECTURE.md            # System architecture diagram
├── WORKFLOW.md                # Agent pipeline workflow diagram
├── .env.example               # Env template (no secrets)
├── .gitignore                 # Ignores .env, output/, __pycache__/
├── requirements.txt           # Python dependencies
├── LICENSE                    # MIT License
│
├── src/
│   ├── __init__.py            # Package init
│   ├── main.py                # CLI entry point
│   ├── config.py              # Environment config loader
│   ├── system.py              # Core orchestrator (4-phase pipeline)
│   ├── agents.py              # All AutoGen agent definitions
│   ├── image_service.py       # DALL-E + Pixabay integration
│   ├── business.py            # Business info & 30+ industry guidance
│   ├── editor.py              # Interactive editing loop
│   └── templates.py           # Theme instructions & fallback HTML
│
└── output/                    # Generated landing pages (git-ignored)
    └── .gitkeep
```

---

## 🔒 Security

- **API keys** are loaded from `.env` via `python-dotenv` — never hardcoded
- **`.env` is git-ignored** — only `.env.example` (with placeholders) is committed
- **`output/`** is git-ignored — generated files stay local

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
