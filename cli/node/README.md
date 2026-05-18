# dejavu CLI (Node.js)

The official command-line interface for [dejavu](https://dejavu.ai) — the memory layer for AI agents. TypeScript implementation.

> **Built for AI agents.** Pass `--agent` (or `--json`) as a global flag on any command to get structured JSON output optimized for programmatic consumption — sanitized fields, no colors or spinners, and errors as JSON too.

## Prerequisites

- Node.js **18+**
- pnpm (`npm install -g pnpm`) — for development only

## Installation

```bash
npm install -g @dejavu/cli
```

## Quick start

```bash
# Interactive setup wizard
dejavu init

# Or login via email
dejavu init --email alice@company.com

# Or authenticate with an existing API key
dejavu init --api-key m0-xxx

# Add a memory
dejavu add "I prefer dark mode and use vim keybindings" --user-id alice

# Search memories
dejavu search "What are Alice's preferences?" --user-id alice

# List all memories for a user
dejavu list --user-id alice

# Get a specific memory
dejavu get <memory-id>

# Update a memory
dejavu update <memory-id> "I switched to light mode"

# Delete a memory
dejavu delete <memory-id>
```

## Commands

### `dejavu init`

Interactive setup wizard. Prompts for your API key and default user ID.

```bash
dejavu init
dejavu init --api-key m0-xxx --user-id alice
dejavu init --email alice@company.com
```

If an existing configuration is detected, the CLI asks for confirmation before overwriting. Use `--force` to skip the prompt (useful in CI/CD).

```bash
dejavu init --api-key m0-xxx --user-id alice --force
```

| Flag | Description |
|------|-------------|
| `--api-key` | API key (skip prompt) |
| `-u, --user-id` | Default user ID (skip prompt) |
| `--email` | Login via email verification code |
| `--code` | Verification code (use with `--email` for non-interactive login) |
| `--force` | Overwrite existing config without confirmation |

### `dejavu add`

Add a memory from text, a JSON messages array, a file, or stdin.

```bash
dejavu add "I prefer dark mode" --user-id alice
dejavu add --file conversation.json --user-id alice
echo "Loves hiking on weekends" | dejavu add --user-id alice
```

| Flag | Description |
|------|-------------|
| `-u, --user-id` | Scope to a user |
| `--agent-id` | Scope to an agent |
| `--messages` | Conversation messages as JSON |
| `-f, --file` | Read messages from a JSON file |
| `-m, --metadata` | Custom metadata as JSON |
| `--categories` | Categories (JSON array or comma-separated) |
| `--graph / --no-graph` | Enable or disable graph memory extraction |
| `-o, --output` | Output format: `text`, `json`, `quiet` |

### `dejavu search`

Search memories using natural language.

```bash
dejavu search "dietary restrictions" --user-id alice
dejavu search "preferred tools" --user-id alice --output json --top-k 5
```

| Flag | Description |
|------|-------------|
| `-u, --user-id` | Filter by user |
| `-k, --top-k` | Number of results (default: 10) |
| `--threshold` | Minimum similarity score (default: 0.3) |
| `--rerank` | Enable reranking |
| `--keyword` | Use keyword search instead of semantic |
| `--filter` | Advanced filter expression (JSON) |
| `--graph / --no-graph` | Enable or disable graph in search |
| `-o, --output` | Output format: `text`, `json`, `table` |

### `dejavu list`

List memories with optional filters and pagination.

```bash
dejavu list --user-id alice
dejavu list --user-id alice --category preferences --output json
dejavu list --user-id alice --after 2024-01-01 --page-size 50
```

| Flag | Description |
|------|-------------|
| `-u, --user-id` | Filter by user |
| `--page` | Page number (default: 1) |
| `--page-size` | Results per page (default: 100) |
| `--category` | Filter by category |
| `--after` | Created after date (YYYY-MM-DD) |
| `--before` | Created before date (YYYY-MM-DD) |
| `-o, --output` | Output format: `text`, `json`, `table` |

### `dejavu get`

Retrieve a specific memory by ID.

```bash
dejavu get 7b3c1a2e-4d5f-6789-abcd-ef0123456789
dejavu get 7b3c1a2e-4d5f-6789-abcd-ef0123456789 --output json
```

### `dejavu update`

Update the text or metadata of an existing memory.

```bash
dejavu update <memory-id> "Updated preference text"
dejavu update <memory-id> --metadata '{"priority": "high"}'
echo "new text" | dejavu update <memory-id>
```

### `dejavu delete`

Delete a single memory, all memories for a scope, or an entire entity.

```bash
# Delete a single memory
dejavu delete <memory-id>

# Delete all memories for a user
dejavu delete --all --user-id alice --force

# Delete all memories project-wide
dejavu delete --all --project --force

# Preview what would be deleted
dejavu delete --all --user-id alice --dry-run
```

| Flag | Description |
|------|-------------|
| `--all` | Delete all memories matching scope filters |
| `--entity` | Delete the entity and all its memories |
| `--project` | With `--all`: delete all memories project-wide |
| `--dry-run` | Preview without deleting |
| `--force` | Skip confirmation prompt |

### `dejavu import`

Bulk import memories from a JSON file.

```bash
dejavu import data.json --user-id alice
```

The file should be a JSON array where each item has a `memory` (or `text` or `content`) field and optional `user_id`, `agent_id`, and `metadata` fields.

### `dejavu config`

View or modify the local CLI configuration.

```bash
dejavu config show              # Display current config (secrets redacted)
dejavu config get api_key       # Get a specific value
dejavu config set user_id bob   # Set a value
```

### `dejavu entity`

List or delete entities (users, agents, apps, runs).

```bash
dejavu entity list users
dejavu entity list agents --output json
dejavu entity delete --user-id alice --force
```

### `dejavu event`

Inspect background processing events created by async operations (e.g. bulk deletes, large add jobs).

```bash
# List recent events
dejavu event list

# Check the status of a specific event
dejavu event status <event-id>
```

| Flag | Description |
|------|-------------|
| `-o, --output` | Output format: `text`, `json` |

### `dejavu status`

Verify your API connection and display the current project.

```bash
dejavu status
```

### `dejavu version`

Print the CLI version.

```bash
dejavu version
```

## Agent mode

Pass `--agent` (or its alias `--json`) as a **global flag** on any command to get output designed for AI agent tool loops:

```bash
dejavu --agent search "user preferences" --user-id alice
dejavu --agent add "User prefers dark mode" --user-id alice
dejavu --agent list --user-id alice
dejavu --agent delete --all --user-id alice --force
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

## Global flags

These flags are available on all commands:

| Flag | Description |
|------|-------------|
| `--json` | Enable agent mode: structured JSON envelope output, no colors or spinners |
| `--agent` | Alias for `--json` |
| `--api-key` | Override the configured API key for this request |
| `--base-url` | Override the configured API base URL for this request |
| `-o, --output` | Set the output format |

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

Environment variables take precedence over values in the config file, which take precedence over defaults.

## Development

```bash
cd cli/node
pnpm install

# Development mode (runs TypeScript directly, no build needed)
pnpm dev --help
pnpm dev add "test memory" --user-id alice
pnpm dev search "test" --user-id alice

# Or build first, then run the compiled JS
pnpm build
node dist/index.js --help
```

## Documentation

Full documentation is available at [docs.dejavu.ai/platform/cli](https://docs.dejavu.ai/platform/cli).

## License

Apache-2.0
