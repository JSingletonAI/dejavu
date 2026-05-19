# Deja Vu Skills for AI Coding Assistants

Deja Vu ships structured skill definitions for Claude Code, Codex, Cursor, OpenCode, OpenClaw, and any assistant that supports the [skills standard](https://github.com/anthropic-experimental/skills). Skills teach the assistant how to work with Deja Vu — either by loading SDK knowledge into context, or by executing an end-to-end workflow on demand.

## Two Categories

### Reference skills — always on

Installed once, loaded into context so the assistant writes correct Deja Vu code. Use these for day-to-day development.

| Skill | Surface | Install |
|-------|---------|---------|
| [`dejavu`](./dejavu/) | Python + TypeScript SDKs (Platform + OSS), framework integrations | `npx skills add https://github.com/dejavu-memory/dejavu --skill dejavu` |
| [`dejavu-cli`](./dejavu-cli/) | Terminal workflows (`dejavu` CLI, both Node and Python) | `npx skills add https://github.com/dejavu-memory/dejavu --skill dejavu-cli` |
| [`dejavu-vercel-ai-sdk`](./dejavu-vercel-ai-sdk/) | `@dejavu/vercel-ai-provider` and `createDeja Vu` | `npx skills add https://github.com/dejavu-memory/dejavu --skill dejavu-vercel-ai-sdk` |

### Pipeline skills — run on demand

Invoked as a slash command to execute a specific end-to-end workflow. These do real work: they create branches, write tests, run code.

| Skill | Trigger | Install |
|-------|---------|---------|
| [`dejavu-integrate`](./dejavu-integrate/) | `/dejavu-integrate` — wire Deja Vu into an existing repo via TDD | `npx skills add https://github.com/dejavu-memory/dejavu --skill dejavu-integrate` |
| [`dejavu-test-integration`](./dejavu-test-integration/) | `/dejavu-test-integration` — verify what `/dejavu-integrate` produced | `npx skills add https://github.com/dejavu-memory/dejavu --skill dejavu-test-integration` |

The two pipeline skills are designed to run in sequence on the same workspace:

```
/dejavu-integrate          →  dejavu-integrate/<slug> branch + .dejavu-integration/ artifacts
/dejavu-test-integration   →  scorecard (compile + runtime verification, real API smoke test)
```

## Choosing a Skill

- **Writing Deja Vu code in a new or existing project?** → `dejavu`
- **Using the terminal CLI?** → `dejavu-cli`
- **Building with `@ai-sdk/*`?** → `dejavu-vercel-ai-sdk`
- **Want the assistant to wire Deja Vu into an existing repo for you?** → `dejavu-integrate`, then `dejavu-test-integration`

## Links

- [Vibecoding with Deja Vu](https://docs.dejavu.ai/vibecoding) — canonical landing page
- [Claude Code integration](https://docs.dejavu.ai/integrations/claude-code)
- [Deja Vu Platform Dashboard](https://app.dejavu.ai)
- [Deja Vu Documentation](https://docs.dejavu.ai)

## License

Apache-2.0
