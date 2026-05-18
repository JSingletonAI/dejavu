# dejavu CLI

The official command-line interface for [dejavu](https://dejavu.ai) — the memory layer for AI agents. Works with the Deja Vu Platform API. Available in Python and Node.js.

> **For AI agents:** pass `--agent` (or `--json`) on any command for structured JSON output purpose-built for tool loops — sanitized fields, no colors or spinners, errors as JSON. See [Agent mode](#agent-mode) below.

## Installation

```bash
npm install -g @dejavu/cli
```

```bash
pip install dejavu-cli
```

Both packages install a `dejavu` binary with identical behavior.

## Quick start

```bash
# Interactive setup wizard
dejavu init

# Or login via email (get a new API key)
dejavu init --email alice@company.com

# Or authenticate with an existing API key
dejavu init --api-key m0-xxx

# Add a memory
dejavu add "I prefer dark mode and use vim keybindings" --user-id alice

# Search memories
dejavu search "What are Alice's preferences?" --user-id alice

# List all memories for a user
dejavu list --user-id alice

# Update a memory
dejavu update <memory-id> "I switched to light mode"

# Delete a memory
dejavu delete <memory-id>
```

## Commands

| Command | Description |
|---------|-------------|
| `dejavu init` | Setup wizard — login via email or configure API key manually |
| `dejavu add` | Add a memory from text, JSON messages, a file, or stdin |
| `dejavu search` | Search memories using natural language |
| `dejavu list` | List memories with optional filters and pagination |
| `dejavu get` | Retrieve a specific memory by ID |
| `dejavu update` | Update the text or metadata of a memory |
| `dejavu delete` | Delete a memory, all memories for a scope, or an entity |
| `dejavu import` | Bulk import memories from a JSON file |
| `dejavu config` | View or modify CLI configuration |
| `dejavu entity` | List or delete entities (users, agents, apps, runs) |
| `dejavu event` | Inspect background processing events (bulk deletes, large add jobs) |
| `dejavu status` | Verify API connection and display current project |
| `dejavu version` | Print the CLI version |

Run `dejavu <command> --help` for detailed usage on any command.

## Agent mode

Pass `--agent` (or its alias `--json`) as a **global flag** on any command to get output designed for AI agent tool loops:

```bash
dejavu --agent search "user preferences" --user-id alice
dejavu --agent add "User prefers dark mode" --user-id alice
dejavu --agent list --user-id alice
```

Every command returns the same envelope shape:

```json
{
  "status": "success",
  "command": "search",
  "duration_ms": 134,
  "scope": { "user_id": "alice" },
  "count": 2,
  "data": [
    { "id": "abc-123", "memory": "User prefers dark mode", "score": 0.97, "created_at": "2026-01-15", "categories": ["preferences"] }
  ]
}
```

What agent mode does differently from `--output json`:
- **Sanitized `data`**: only the fields an agent needs (id, memory, score, etc.) — no internal API noise
- **No human output**: spinners, colors, and banners are suppressed entirely
- **Errors as JSON**: errors go to stdout as `{"status": "error", "command": "...", "error": "..."}` with a non-zero exit code

Use `dejavu help --json` to get the full command tree as JSON — useful for agents that need to self-discover available commands.

## Output formats

Control how results are displayed with `--output`:

| Format | Description |
|--------|-------------|
| `text` | Human-readable with colors and formatting (default) |
| `json` | Structured JSON for piping to `jq` (raw API response) |
| `table` | Tabular format (default for `list`) |
| `quiet` | Minimal — just IDs or status codes |
| `agent` | Structured JSON envelope with sanitized fields (set by `--agent`/`--json`) |

## Environment variables

| Variable | Description |
|----------|-------------|
| `VENICE_API_KEY` | API key (overrides config file) |
| `DEJAVU_BASE_URL` | API base URL |
| `DEJAVU_USER_ID` | Default user ID |
| `DEJAVU_AGENT_ID` | Default agent ID |
| `DEJAVU_APP_ID` | Default app ID |
| `DEJAVU_RUN_ID` | Default run ID |
| `DEJAVU_ENABLE_GRAPH` | Enable graph memory (`true` / `false`) |

## Implementations

| Language | Directory | Package | Docs |
|----------|-----------|---------|------|
| TypeScript | [`node/`](./node/) | `@dejavu/cli` | [README](./node/README.md) |
| Python | [`python/`](./python/) | `dejavu-cli` | [README](./python/README.md) |

## Documentation

Full documentation is available at [docs.dejavu.ai/platform/cli](https://docs.dejavu.ai/platform/cli).

## License

Apache-2.0
