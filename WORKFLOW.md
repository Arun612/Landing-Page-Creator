# Agent Workflow & Pipeline

## Pipeline Overview

The landing page generation follows a **4-phase pipeline** designed for maximum parallelism and quality. Each phase builds on the outputs of the previous one.

```mermaid
flowchart TD
    START(["🚀 User Input<br/><i>Business info, theme, image pref</i>"]) --> ENRICH

    subgraph PREP["Phase 0 — Preparation"]
        ENRICH["Enhance Business Context<br/><i>Fuzzy-match 30+ industry profiles</i>"]
        THEME["Load Theme Instructions<br/><i>Light / Dark CSS directives</i>"]
        ENRICH --> THEME
    end

    THEME --> P1

    subgraph P1["Phase 1 — Strategy + Content  ⚡ PARALLEL"]
        direction LR
        SA["🎯 Strategy Agent<br/><i>Market positioning<br/>Audience psychology<br/>Conversion pathway</i>"]
        CA["✍️ Content Agent<br/><i>Headlines & copy<br/>Benefits & CTAs<br/>Social proof framework</i>"]
    end

    P1 --> VAL1{"Content<br/>validation"}
    VAL1 -- "Too short" --> RETRY1["Retry agent<br/>with emphasis"]
    RETRY1 --> P2
    VAL1 -- "OK" --> P2

    subgraph P2["Phase 2 — Sections + Image  ⚡ PARALLEL (7 workers)"]
        direction LR
        IA["🖼️ Image Agent<br/><i>DALL-E prompts<br/>Pixabay keywords</i>"]

        subgraph SECTS["Section Agents"]
            NAV["🧭 Navbar"]
            HERO["🦸 Hero"]
            FEAT["⭐ Features"]
            TEST["💬 Testimonials"]
            CTA["📞 CTA"]
            FOOT["🔗 Footer"]
        end

        IMG_SVC["ImageService<br/><i>DALL-E → Pixabay → Fallback</i>"]
        IA --> IMG_SVC
    end

    P2 --> P3

    subgraph P3["Phase 3 — Integration"]
        INT["🏗️ Integrator Agent<br/><i>Assembles all sections into<br/>complete production HTML<br/>(2000+ words, responsive,<br/>glassmorphism, animations)</i>"]
    end

    P3 --> P4

    subgraph P4["Phase 4 — Post-Integration QA"]
        REV["🔍 Review Agent<br/><i>Validates assembled HTML:<br/>• HTML syntax & semantics<br/>• Bootstrap class correctness<br/>• Accessibility (ARIA, alt text)<br/>• Brand/business alignment<br/>• Theme consistency<br/>• Outputs corrected HTML</i>"]
    end

    P4 --> VERDICT{"Verdict"}
    VERDICT -- "SHIP_IT" --> SAVE
    VERDICT -- "NEEDS_FIXES" --> APPLY["Apply corrected HTML"]
    APPLY --> SAVE

    SAVE["💾 Save HTML to output/"] --> EDIT_Q{"User wants<br/>to edit?"}
    EDIT_Q -- "Yes" --> EDIT_LOOP
    EDIT_Q -- "No" --> DONE(["✅ Done"])

    subgraph EDIT_LOOP["Interactive Editing Loop"]
        direction TB
        REQ["User describes change<br/><i>in plain English</i>"]
        APPLY_EDIT["Integrator Agent<br/>applies change"]
        SAVE_EDIT["Save updated HTML"]
        REQ --> APPLY_EDIT --> SAVE_EDIT
        SAVE_EDIT -- "More edits" --> REQ
    end

    EDIT_LOOP -- "Exit" --> DONE

    style PREP fill:#f0f4ff,stroke:#4a6cf7
    style P1 fill:#ecfdf5,stroke:#059669
    style P2 fill:#fff7ed,stroke:#f59e0b
    style P3 fill:#fdf2f8,stroke:#ec4899
    style P4 fill:#fef2f2,stroke:#ef4444
    style EDIT_LOOP fill:#f5f3ff,stroke:#8b5cf6
```

---

## Phase Details

### Phase 0 — Preparation

| Step | Module | Description |
|------|--------|-------------|
| Business Enhancement | `business.py` | Fuzzy-matches the business type against 30+ industry profiles and attaches guidance (tone, focus areas, CTA style, social proof type, urgency type) |
| Theme Loading | `templates.py` | Loads detailed CSS design directives for the chosen theme |

### Phase 1 — Strategy + Content ⚡

**Execution:** Two agents run in **parallel** via `ThreadPoolExecutor(max_workers=2)`.

| Agent | Input | Output |
|-------|-------|--------|
| **Strategy Agent** | Business context + industry guidance | Market positioning, audience psychology, conversion pathway, urgency mechanisms |
| **Content Agent** | Business context + industry guidance | Headlines, subheadlines, hero copy, 3 key benefits, social proof concepts, CTA variations |

**Validation:** If either response is < 100 characters, it is automatically retried with an emphasis prompt.

### Phase 2 — Sections + Image ⚡

**Execution:** 7 agents run in **parallel** via `ThreadPoolExecutor(max_workers=7)`.

| Agent | Output |
|-------|--------|
| **Image Agent** | DALL-E prompt + Pixabay keywords (parsed by `ImageService`) |
| **Navbar Agent** | Navigation structure description |
| **Hero Agent** | Hero section layout description |
| **Features Agent** | Features section layout description |
| **Testimonials Agent** | Testimonials section layout description |
| **CTA Agent** | Call-to-action section layout description |
| **Footer Agent** | Footer section layout description |

**Image Resolution:** After the Image Agent responds, `ImageService` attempts acquisition in this order:

```mermaid
flowchart LR
    A["User choice"] --> B{"DALL-E?"}
    B -- Yes --> C["Generate with DALL-E 3"]
    C -- Success --> DONE["✅ Use image"]
    C -- Fail --> D{"Pixabay?"}
    B -- No --> D
    D -- Yes --> E["Search Pixabay"]
    E -- Found --> DONE
    E -- Empty --> F["Fallback: LLM keyword extraction → Pixabay"]
    F -- Found --> DONE
    F -- Empty --> G["❌ No image"]
```

### Phase 3 — Integration

The **Integrator Agent** receives:
- All section descriptions from Phase 2
- Strategy + content from Phase 1
- Hero image URL (if acquired)
- Theme instructions
- Industry guidance

It outputs a **complete, single-file HTML document** with:
- Tailwind CSS + Bootstrap Icons via CDN
- Custom CSS variables for theming
- Glassmorphism effects
- Scroll-triggered animations (Intersection Observer)
- Mobile-first responsive design
- 2000+ words of content

### Phase 4 — Post-Integration QA

> **Workflow improvement:** In the original design, the Review Agent reviewed text *descriptions* before integration — meaning it couldn't catch HTML rendering bugs, broken Bootstrap classes, or integration conflicts. Now it reviews the *assembled HTML*, providing far more valuable QA.

The **Review Agent** inspects the complete HTML and outputs:
- Critical errors list
- Section-by-section review (PASS / issues)
- Technical and business alignment scores (1-10)
- Verdict: `SHIP_IT` or `NEEDS_FIXES`
- If `NEEDS_FIXES`: a corrected HTML document

### Interactive Editing (Optional)

After generation, users can enter a conversational editing loop:

1. Describe a change in plain English (e.g., "Make the hero background gradient purple")
2. The Integrator Agent applies the change to the current HTML
3. The updated file is auto-saved
4. Repeat up to 10 times

---

## Agent Communication Pattern

All agents communicate through AutoGen's `UserProxyAgent.initiate_chat()` with `max_turns=1` (single-shot). The orchestrator (`system.py`) manages the conversation flow — agents do not talk to each other directly.

```mermaid
sequenceDiagram
    participant O as Orchestrator<br/>(system.py)
    participant UP as UserProxy
    participant A as Agent

    O->>UP: initiate_chat(agent, message)
    UP->>A: Deliver message
    A->>A: Process with GPT
    A->>UP: Return response
    UP->>O: Return chat result
    O->>O: Extract content,<br/>pass to next phase
```

This hub-and-spoke pattern keeps agents stateless and independently testable.
