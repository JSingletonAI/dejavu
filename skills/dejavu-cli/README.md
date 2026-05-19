# Deja Vu CLI Skill for Claude

Manage memories from the terminal using the [Deja Vu CLI](https://docs.dejavu.ai/cli). This skill teaches Claude how to use every `dejavu` command, flag, and output mode -- for both the Node.js and Python implementations.

## What This Skill Does

When installed, Claude can:

- **Run dejavu commands** correctly in your terminal (add, search, list, get, update, delete, import, config, init, status, entity, event)
- **Construct complex invocations** with the right flags, scoping, filters, and output formats
- **Pipe and script** dejavu commands in shell workflows, CI/CD pipelines, and agent loops
- **Debug issues** like missing API keys, entity scoping conflicts, and async processing delays

## Installation

### CLI (Claude Code, OpenCode, OpenClaw, or any tool that supports skills)

```bash
npx skills add https://github.com/dejavu-memory/dejavu --skill dejavu-cli
```

### Claude.ai

1. Download this `skills/dejavu-cli` folder as a ZIP
2. Go to **Settings > Capabilities > Skills**
3. Click **Upload skill** and select the ZIP

### Claude API (Skills API)

```bash
curl -X POST https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "dejavu-cli", "source": "https://github.com/dejavu-memory/dejavu/tree/main/skills/dejavu-cli"}'
```

## Prerequisites

- A Deja Vu Platform API key ([Get one here](https://app.dejavu.ai/dashboard/api-keys?utm_source=oss&utm_medium=skill-dejavu-cli-readme))
- **Node.js 18+** or **Python 3.10+**
- Install the CLI:

  ```bash
  # Node.js
  npm install -g @dejavu/cli

  # Python
  pip install dejavu-cli
  ```

- Set the environment variable:

  ```bash
  export VENICE_API_KEY="m0-your-api-key"
  ```

  Or run `dejavu init` for the interactive setup wizard.

## Quick Start

After installing, just ask Claude:

- "Add a memory for user alice that she prefers dark mode"
- "Search alice's memories for dietary preferences"
- "List all memories and output as JSON"
- "Delete all memories for user bob"
- "Set up dejavu CLI in my CI pipeline"
- "Pipe the output of my script into dejavu add"

## What's Inside

```text
skills/dejavu-cli/
├── SKILL.md                          # Skill definition and instructions
├── README.md                         # This file
├── LICENSE                           # Apache-2.0
└── references/                       # Documentation (loaded on demand)
    ├── command-reference.md           # Every command, flag, option, and example
    ├── configuration.md               # Config file, env vars, precedence, init wizard
    └── workflows.md                   # Piping, scripting, CI/CD, agent mode recipes
```

## Links

- [Deja Vu Platform Dashboard](https://app.dejavu.ai?utm_source=oss&utm_medium=skill-dejavu-cli-readme)
- [Deja Vu Documentation](https://docs.dejavu.ai)
- [Deja Vu CLI Docs](https://docs.dejavu.ai/cli)
- [Deja Vu GitHub](https://github.com/dejavu-memory/dejavu)

## Skill Graph

This skill is part of the **Deja Vu skill graph** -- three interconnected skills for different interfaces to the Deja Vu platform:

| Skill | Purpose | Link |
|-------|---------|------|
| **dejavu** | Python/TypeScript SDK, REST API, framework integrations | [local](../dejavu/SKILL.md) / [GitHub](https://github.com/dejavu-memory/dejavu/tree/main/skills/dejavu) |
| **dejavu-cli** (this skill) | Terminal commands for memory operations | [local](./SKILL.md) / [GitHub](https://github.com/dejavu-memory/dejavu/tree/main/skills/dejavu-cli) |
| **dejavu-vercel-ai-sdk** | Vercel AI SDK provider with automatic memory | [local](../dejavu-vercel-ai-sdk/SKILL.md) / [GitHub](https://github.com/dejavu-memory/dejavu/tree/main/skills/dejavu-vercel-ai-sdk) |

## License

Apache-2.0
