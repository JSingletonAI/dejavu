# Deja Vu CLI Configuration

Everything about configuring the dejavu CLI: config file format, environment variables, the init wizard, and precedence rules.

---

## Config File Location

| Path | Permissions | Description |
|------|-------------|-------------|
| `~/.dejavu/` | `0700` (owner rwx) | Config directory. Created automatically by `dejavu init`. |
| `~/.dejavu/config.json` | `0600` (owner rw) | Config file. Contains API key, defaults, and platform settings. |

The restricted permissions ensure API keys are not world-readable.

---

## Config File Schema

```json
{
  "version": 1,
  "defaults": {
    "user_id": "",
    "agent_id": "",
    "app_id": "",
    "run_id": ""
  },
  "platform": {
    "api_key": "",
    "base_url": "https://api.dejavu.ai"
  }
}
```

### Field Reference

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `version` | integer | `1` | Config schema version. |
| `defaults.user_id` | string | `""` | Default user ID for scoping commands. |
| `defaults.agent_id` | string | `""` | Default agent ID for scoping commands. |
| `defaults.app_id` | string | `""` | Default app ID for scoping commands. |
| `defaults.run_id` | string | `""` | Default run ID for scoping commands. |
| `platform.api_key` | string | `""` | API key for the Deja Vu Platform. |
| `platform.base_url` | string | `"https://api.dejavu.ai"` | Base URL for API requests. |

---

## `dejavu init` Wizard

The `init` command provides two authentication flows:

### API Key Flow (default)

```bash
# Fully interactive:
dejavu init

# Fully non-interactive:
dejavu init --api-key m0-xxx --user-id alice
```

**Interactive mode steps:**

1. Displays the dejavu banner.
2. Checks for existing config. If found with an API key, asks for confirmation to overwrite.
3. Prompts for API key (input masked with `*` characters; supports backspace and Ctrl+U to clear).
4. Prompts for default user ID (default value: `dejavu-cli`).
5. Validates the connection by calling the status endpoint.
6. Saves config to `~/.dejavu/config.json` with `0600` permissions.
7. Prints success message.

**Non-interactive mode:** When both `--api-key` and `--user-id` are provided, skips all prompts and saves directly. When running in a non-TTY without both flags, prints an error:

```
Non-interactive terminal detected and missing required flags.
Usage: dejavu init --api-key <key> --user-id <id>
```

### Email Login Flow

```bash
# Interactive (prompts for code):
dejavu init --email alice@company.com

# Fully non-interactive:
dejavu init --email alice@company.com --code 482901
```

**Steps:**

1. Sends a 6-digit verification code to the email via `POST /api/v1/auth/email_code/`.
2. If `--code` is provided, verifies immediately. Otherwise prompts for the code.
3. On success: receives API key, org_id, and project_id from the server.
4. Saves to config. Creates a new account if the email is not registered.

Cannot be combined with `--api-key`.

### Force Overwrite

If `~/.dejavu/config.json` already exists with an API key, `dejavu init` warns and asks for confirmation. Use `--force` to skip:

```bash
dejavu init --api-key m0-new-key --user-id alice --force
```

---

## `dejavu config` Subcommands

### `dejavu config show`

Displays the current configuration as a formatted table (text mode) or JSON envelope (json mode). API keys are always redacted.

```bash
dejavu config show
dejavu config show -o json
```

### `dejavu config get <key>`

Reads a single configuration value. The key uses dotted notation.

```bash
dejavu config get platform.api_key     # prints: m0-x...xxxx (redacted)
dejavu config get defaults.user_id     # prints: alice
```

**Valid keys:**
- `platform.api_key`
- `platform.base_url`
- `defaults.user_id`
- `defaults.agent_id`
- `defaults.app_id`
- `defaults.run_id`

Unknown keys print an error message.

### `dejavu config set <key> <value>`

Sets a configuration value and saves the config file.

```bash
dejavu config set defaults.user_id alice
dejavu config set platform.base_url https://api.dejavu.ai
```

**Type coercion:**
- Boolean fields accept `true`, `1`, `yes` (case-insensitive) as true. Anything else is false.
- Integer fields are parsed with `parseInt`.
- String fields are stored as-is.

### `dejavu config clear`

Removes the config file (`~/.dejavu/config.json`).

```bash
dejavu config clear
```

---

## Environment Variables

Environment variables override config file values but are overridden by CLI flags.

| Variable | Config Path | Type | Default |
|----------|-------------|------|---------|
| `VENICE_API_KEY` | `platform.api_key` | string | `""` |
| `DEJAVU_BASE_URL` | `platform.base_url` | string | `"https://api.dejavu.ai"` |
| `DEJAVU_USER_ID` | `defaults.user_id` | string | `""` |
| `DEJAVU_AGENT_ID` | `defaults.agent_id` | string | `""` |
| `DEJAVU_APP_ID` | `defaults.app_id` | string | `""` |
| `DEJAVU_RUN_ID` | `defaults.run_id` | string | `""` |

---

## Precedence

Configuration values are resolved in this order (highest priority first):

```
1. CLI flags        --api-key, --user-id, --base-url, etc.
2. Environment vars VENICE_API_KEY, DEJAVU_USER_ID, etc.
3. Config file      ~/.dejavu/config.json
4. Defaults         Hardcoded defaults (empty strings, false, https://api.dejavu.ai)
```

**Example:** If your config file has `user_id: "bob"`, the env var `DEJAVU_USER_ID=charlie` is set, and you pass `--user-id alice` on the command line, the effective user_id is `alice`.

---

## API Key Redaction Rules

Whenever an API key is displayed (in `config show`, `config get`, status output, etc.), it is redacted:

| Condition | Output |
|-----------|--------|
| Empty string | `(not set)` |
| Length <= 8 | First 2 characters + `***` |
| Length > 8 | First 4 characters + `...` + last 4 characters |

**Examples:**
- `""` -> `(not set)`
- `"m0-abc"` -> `m0***`
- `"m0-abcdefghijklmnop"` -> `m0-a...mnop`

The redaction function is named `redact_key` (Python) / `redactKey` (Node).

---

## Dotted Key Map

The `config get` and `config set` commands use dotted key paths. Here is the full mapping:

| Dotted Key | Section | Field |
|------------|---------|-------|
| `platform.api_key` | platform | api_key |
| `platform.base_url` | platform | base_url |
| `defaults.user_id` | defaults | user_id |
| `defaults.agent_id` | defaults | agent_id |
| `defaults.app_id` | defaults | app_id |
| `defaults.run_id` | defaults | run_id |
