# Deja Vu

[![Website](https://img.shields.io/badge/website-deja--vu.dev-0f172a?style=flat-square)](https://deja-vu.dev)
[![GitHub](https://img.shields.io/badge/GitHub-JSingletonAI-0f172a?style=flat-square&logo=github&logoColor=white)](https://github.com/JSingletonAI)
[![License](https://img.shields.io/badge/license-Apache--2.0-0f172a?style=flat-square)](LICENSE)
<img width="1983" height="793" alt="GithubImage2" src="https://github.com/user-attachments/assets/831be4fe-7384-428b-8e97-864c22255d84" />

**CA:** `0x337e3CBbf784aA6C066F788e9AaD6e84A308AB07`

Local-first AI memory for agents and assistants.

Your AI tools forget everything between sessions. The ones that don't store your context on someone else's servers. Deja Vu is the third option — a memory layer that runs on your machine, in SQLite, and plugs into anything that speaks Python, REST, CLI, or MCP.

**One memory store, every tool.** Add a preference from the CLI, retrieve it in Claude Desktop, query it from a Python agent — same database, no sync, no account. Context built up in one tool is immediately available in the next.

**Private by default.** Memories live in `~/.dejavu` on your machine. The only thing that leaves is the LLM call itself, routed through Venice's privacy-focused API. No telemetry, no hosted memory service, no vendor lock-in. Open the SQLite file with any client and inspect every byte.

## Quick start

```bash
pip install dejavu-memory
dejavu init
dejavu add "I prefer concise technical explanations"
dejavu search "How should responses be written for me?"
```

That's it. Memories are saved to `~/.dejavu/` and searchable immediately.

### Set your Venice API key

Deja Vu uses Venice for memory extraction and reasoning. Get a key at [venice.ai](https://venice.ai) and export it:

```bash
export VENICE_API_KEY="your-key"
```

## Python

```python
from dejavu import Memory

memory = Memory()
memory.add("I prefer local-first tools.", user_id="local_user")

results = memory.search("What tools do I prefer?", user_id="local_user")
print(results)
```

## Local REST API

```bash
dejavu serve
curl http://127.0.0.1:8765/health
```

Runs on `127.0.0.1` by default — not exposed to your network.

## How it works

Deja Vu is three layers: an interface layer (Python, CLI, REST, MCP), a memory engine that extracts and ranks what's worth remembering, and a local SQLite store. Venice handles the LLM calls for extraction and search — everything else runs on your machine.
<img width="929" height="695" alt="image" src="https://github.com/user-attachments/assets/eb7aed95-eac3-48a8-8fde-fdecfdd8b1e8" />

When you add a memory, the engine asks Venice to pull out durable facts and preferences from the raw text, then writes them to SQLite with embeddings. When you search, it embeds the query, pulls the closest matches, and optionally re-ranks them through Venice for relevance.

Every interface hits the same engine and the same store. Add a memory through the CLI, retrieve it from Claude Desktop over MCP — same database, no sync.

## MCP

Run Deja Vu as an MCP server so local agents and editors share the same memory store.

```json
{
  "mcpServers": {
    "dejavu": {
      "command": "dejavu",
      "args": ["mcp"],
      "env": {
        "VENICE_API_KEY": "your-key"
      }
    }
  }
}
```

Drop this into your Claude Desktop, Cursor, or any MCP-compatible client config.

## Interfaces

| Interface | Use it for |
| --- | --- |
| Python SDK | Embedding memory directly into agents and scripts |
| CLI (`dejavu`) | Quick adds, searches, and inspection from the terminal |
| REST API | Language-agnostic access, local services, internal tools |
| MCP server | Sharing one memory store across Claude Desktop, Cursor, and other MCP clients |

## Privacy

- Memories stored locally under `~/.dejavu`
- No hosted memory account required
- Telemetry off by default
- LLM calls go through Venice only

## Project structure

Deja Vu writes everything to `~/.dejavu/`:

```
~/.dejavu/
├── config.json   <- Venice key, model choices, local settings
├── memories.db   <- SQLite store: memories, embeddings, metadata
└── logs/         <- request logs (off by default, opt-in via config)
```

The repo itself:

<img width="538" height="798" alt="image" src="https://github.com/user-attachments/assets/1658bf57-20a0-4560-bf48-dc4338666b25" />

```
dejavu/           <- core Python SDK and local memory engine
cli/              <- Python and Node CLIs
docs/             <- documentation
examples/         <- demo apps and integration samples
tests/            <- SDK and interface tests
```

## Background

Memory is the missing layer of the AI stack. Models get smarter every month and forget you every session. The few that remember keep your context on their servers, on their terms. Deja Vu builds the layer that should have existed from the start: a personal memory store you own, run locally, and carry into every tool that can talk to it. The long-term goal is a portable memory standard for AI, where your context is infrastructure you control rather than a feature locked inside someone else's product. This first release ships the foundation. Local storage, open interfaces, zero lock-in.

![Deja Vu - Memories owned by me](docs/images/dejavu-hero.png)

## Maintainer

- [JSingletonAI](https://github.com/JSingletonAI)

## Attribution

Deja Vu builds on the open-source work of [`mem0ai/mem0`](https://github.com/mem0ai/mem0), re-architected around a local-first, privacy-preserving design. Released under Apache-2.0.

