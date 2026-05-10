# System Architecture

## Component Overview

The system is composed of five layers — **Configuration**, **External Services**, **Agent Layer**, **Service Layer**, and **Orchestration** — that work together to transform a business description into a production-ready HTML landing page.

```mermaid
graph TB
    subgraph Config["⚙️ Configuration Layer"]
        ENV[".env file"]
        CFG["config.py<br/><i>Config dataclass</i>"]
        ENV --> CFG
    end

    subgraph External["☁️ External Services"]
        GPT["Azure OpenAI<br/><b>GPT-5 Mini</b>"]
        DALLE["Azure OpenAI<br/><b>DALL-E 3</b>"]
        PIX["Pixabay<br/><b>Stock Photos API</b>"]
    end

    subgraph Agents["🤖 Agent Layer — agents.py"]
        UP["UserProxy<br/>ProjectManager"]
        SA["Strategy Agent<br/><i>#1 — Market positioning</i>"]
        CA["Content Agent<br/><i>#2 — Copywriting</i>"]
        IA["Image Agent<br/><i>#3 — Visual strategy</i>"]

        subgraph Sections["Section Agents #4a-f"]
            NAV["Navbar"]
            HERO["Hero"]
            FEAT["Features"]
            TEST["Testimonials"]
            CTA["CTA"]
            FOOT["Footer"]
        end

        INT["Integrator Agent<br/><i>#5 — HTML assembly</i>"]
        REV["Review Agent<br/><i>#6 — Post-integration QA</i>"]
    end

    subgraph Services["🔧 Service Layer"]
        IMG["image_service.py<br/><i>ImageService class</i>"]
        BIZ["business.py<br/><i>Industry guidance map</i>"]
        TPL["templates.py<br/><i>Theme instructions</i>"]
        EDT["editor.py<br/><i>Interactive editor</i>"]
    end

    subgraph Core["🎯 Orchestration Layer"]
        SYS["system.py<br/><b>EnhancedLandingPageCreatorSystem</b>"]
        MAIN["main.py<br/><i>CLI entry point</i>"]
    end

    CFG --> SYS
    SYS --> UP
    SYS --> IMG
    SYS --> BIZ
    SYS --> TPL
    SYS --> EDT

    UP --> SA
    UP --> CA
    UP --> IA
    UP --> NAV
    UP --> HERO
    UP --> FEAT
    UP --> TEST
    UP --> CTA
    UP --> FOOT
    UP --> INT
    UP --> REV

    SA --> GPT
    CA --> GPT
    IA --> GPT
    NAV --> GPT
    HERO --> GPT
    FEAT --> GPT
    TEST --> GPT
    CTA --> GPT
    FOOT --> GPT
    INT --> GPT
    REV --> GPT

    IMG --> DALLE
    IMG --> PIX
    IMG --> GPT

    MAIN --> SYS

    style Config fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style External fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
    style Agents fill:#f0fdf4,stroke:#059669,stroke-width:2px
    style Services fill:#fdf2f8,stroke:#ec4899,stroke-width:2px
    style Core fill:#fef2f2,stroke:#ef4444,stroke-width:2px
```

---

## Component Descriptions

### Configuration Layer

| Component | File | Responsibility |
|-----------|------|----------------|
| **Environment** | `.env` | Stores API keys and endpoints (git-ignored) |
| **Config** | `config.py` | Loads, validates, and exposes settings via a frozen `Config` dataclass |

### External Services

| Service | Purpose | Required? |
|---------|---------|-----------|
| **Azure OpenAI (GPT)** | Powers all 9 AutoGen agents | ✅ Yes |
| **Azure OpenAI (DALL-E 3)** | AI-generated hero images | ❌ Optional |
| **Pixabay API** | Professional stock photo fallback | ❌ Optional |

### Agent Layer

| Agent | Role | Phase |
|-------|------|-------|
| **UserProxy** | Manages agent conversations, collects responses | All |
| **Strategy Agent** | Market positioning, audience psychology, conversion strategy | 1 |
| **Content Agent** | Headlines, copy, CTAs, benefit frameworks | 1 |
| **Image Agent** | DALL-E prompts and Pixabay keywords | 2 |
| **Section Agents** (×6) | Navbar, Hero, Features, Testimonials, CTA, Footer design specs | 2 |
| **Integrator Agent** | Assembles all inputs into complete production HTML | 3 |
| **Review Agent** | Post-integration QA — validates HTML, accessibility, brand fit | 4 |

### Service Layer

| Module | Class/Functions | Responsibility |
|--------|-----------------|----------------|
| `image_service.py` | `ImageService` | DALL-E generation, Pixabay fetching, keyword extraction, fallback chains |
| `business.py` | `enhance_business_context()` | 30+ industry guidance profiles, interactive business info collection |
| `templates.py` | `get_theme_instructions()` | Light/Dark theme CSS directives, fallback HTML generator |
| `editor.py` | `LandingPageEditor` | Conversational editing loop for post-generation refinement |

### Orchestration Layer

| Module | Class | Responsibility |
|--------|-------|----------------|
| `system.py` | `EnhancedLandingPageCreatorSystem` | Wires all layers, runs the 4-phase pipeline, manages state |
| `main.py` | `main()` | CLI interface, user prompts, program flow |

---

## Data Flow

```mermaid
flowchart LR
    A["User Input<br/><i>business info, theme,<br/>image preference</i>"] --> B["Config<br/>Validation"]
    B --> C["Business<br/>Enhancement"]
    C --> D["Agent<br/>Pipeline"]
    D --> E["HTML<br/>Output"]
    E --> F["Optional<br/>Editing"]
    F --> G["Final<br/>Landing Page"]
```

---

## Technology Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.10+ |
| **LLM Framework** | Microsoft AutoGen |
| **LLM Provider** | Azure OpenAI (GPT-5 Mini) |
| **Image Generation** | Azure DALL-E 3 |
| **Stock Photos** | Pixabay API |
| **Config Management** | python-dotenv |
| **HTTP Client** | requests |
| **Concurrency** | concurrent.futures (ThreadPoolExecutor) |
| **Output Format** | Single-file HTML (Tailwind CSS + Bootstrap Icons) |
