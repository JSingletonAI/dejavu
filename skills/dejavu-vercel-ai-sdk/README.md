# Deja Vu Vercel AI SDK Skill for Claude

Add persistent memory to any Vercel AI SDK application using [@dejavu/vercel-ai-provider](https://www.npmjs.com/package/@dejavu/vercel-ai-provider).

## What This Skill Does

When installed, Claude can:

- **Set up `@dejavu/vercel-ai-provider`** in your TypeScript or Next.js project
- **Generate working code** using the wrapped model (`createDeja Vu`) or standalone utilities (`retrieveMemories`, `addMemories`, etc.)
- **Configure multi-provider setups** (OpenAI, Anthropic, Google, Groq, Cohere)
- **Integrate memory** into streaming responses, structured output, and API routes

## Installation

### CLI (Claude Code, OpenCode, OpenClaw, or any tool that supports skills)

```bash
npx skills add https://github.com/dejavu-memory/dejavu --skill dejavu-vercel-ai-sdk
```

### Claude.ai

1. Download this `skills/dejavu-vercel-ai-sdk` folder as a ZIP
2. Go to **Settings > Capabilities > Skills**
3. Click **Upload skill** and select the ZIP

### Claude API (Skills API)

```bash
curl -X POST https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "dejavu-vercel-ai-sdk", "source": "https://github.com/dejavu-memory/dejavu/tree/main/skills/dejavu-vercel-ai-sdk"}'
```

### Prerequisites

- **Node.js 18+**
- **Vercel AI SDK v5** (`ai` package version 5.x)
- A Deja Vu Platform API key ([Get one here](https://app.dejavu.ai/dashboard/api-keys?utm_source=oss&utm_medium=skill-dejavu-vercel-ai-sdk-readme))
- An LLM provider API key (OpenAI, Anthropic, Google, Groq, or Cohere)
- Set environment variables:

  ```bash
  export VENICE_API_KEY="m0-xxx"
  export OPENAI_API_KEY="sk-xxx"  # or your chosen provider's key
  ```

## Quick Start

After installing, just ask Claude:

- "Add memory to my Vercel AI SDK app"
- "Set up dejavu with streamText in my Next.js API route"
- "Use retrieveMemories with Anthropic instead of the wrapped model"
- "Show me how to use graph memories with the Vercel AI provider"
- "Help me store conversation history with addMemories"

## What's Inside

```text
skills/dejavu-vercel-ai-sdk/
├── SKILL.md                          # Skill definition and instructions
├── README.md                         # This file
├── LICENSE                           # Apache-2.0
└── references/                       # Documentation (loaded on demand)
    ├── provider-api.md               # createDeja Vu, Deja VuProvider, types, config
    ├── memory-utilities.md           # addMemories, retrieveMemories, getMemories, searchMemories
    └── usage-patterns.md             # Working examples: streaming, Next.js, multi-provider, graph
```

## Links

- [Deja Vu Platform Dashboard](https://app.dejavu.ai?utm_source=oss&utm_medium=skill-dejavu-vercel-ai-sdk-readme)
- [Deja Vu Documentation](https://docs.dejavu.ai)
- [Deja Vu GitHub](https://github.com/dejavu-memory/dejavu)
- [@dejavu/vercel-ai-provider on npm](https://www.npmjs.com/package/@dejavu/vercel-ai-provider)
- [Vercel AI SDK Documentation](https://ai-sdk.dev/docs)

## Skill Graph

This skill is part of the Deja Vu skill graph. The three Deja Vu skills (dejavu, dejavu-cli, dejavu-vercel-ai-sdk) each cover a different interface to the same Deja Vu Platform API.

## License

Apache-2.0
