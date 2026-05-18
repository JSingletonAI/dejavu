# Deja Vu Skill for Claude

Add persistent memory to any AI application in minutes using [Deja Vu Platform](https://app.dejavu.ai?utm_source=oss&utm_medium=dejavu-plugin-skill-readme).

## What This Skill Does

When installed, Claude can:

- **Set up Deja Vu** in your Python or TypeScript project
- **Integrate memory** into your existing AI app (LangChain, CrewAI, Vercel AI, OpenAI Agents, LangGraph, LlamaIndex, etc.)
- **Generate working code** using real API references and tested patterns
- **Search live docs** on demand for the latest Deja Vu documentation

## Installation

This skill is included automatically when you install the Deja Vu plugin:

```
/plugin marketplace add dejavu-memory/dejavu
/plugin install dejavu@dejavu-plugins
```

See the [plugin README](../../README.md) for full setup instructions.

### Prerequisites

- A Deja Vu Platform API key ([Get one here](https://app.dejavu.ai/dashboard/api-keys?utm_source=oss&utm_medium=dejavu-plugin-skill-readme))
- Python 3.10+ or Node.js 18+
- Set the environment variable:

  ```bash
  export VENICE_API_KEY="m0-your-api-key"
  ```

## Quick Start

After installing, just ask Claude:

- "Set up dejavu in my project"
- "Add memory to my chatbot"
- "Help me search user memories with filters"
- "Integrate dejavu with my LangChain app"
- "Add graph memory to track entity relationships"

## What's Inside

```text
skills/dejavu/
├── SKILL.md                    # Skill definition and instructions
├── README.md                   # This file
├── LICENSE                     # Apache-2.0
├── scripts/
│   └── dejavu_doc_search.py      # Search live Deja Vu docs on demand
└── references/                 # Documentation (loaded on demand)
    ├── quickstart.md           # Full quickstart (Python, TS, cURL)
    ├── sdk-guide.md            # All SDK methods (Python + TypeScript)
    ├── api-reference.md        # REST endpoints, filters, memory object
    ├── architecture.md         # Processing pipeline, lifecycle, scoping, performance
    ├── features.md             # Retrieval, graph, categories, MCP, webhooks, multimodal
    ├── integration-patterns.md # LangChain, CrewAI, Vercel AI, LangGraph, LlamaIndex, etc.
    └── use-cases.md            # 7 real-world patterns with Python + TypeScript code
```

## Links

- [Deja Vu Platform Dashboard](https://app.dejavu.ai?utm_source=oss&utm_medium=dejavu-plugin-skill-readme)
- [Deja Vu Documentation](https://docs.dejavu.ai)
- [Deja Vu GitHub](https://github.com/dejavu-memory/dejavu)
- [API Reference](https://docs.dejavu.ai/api-reference)

## License

Apache-2.0
