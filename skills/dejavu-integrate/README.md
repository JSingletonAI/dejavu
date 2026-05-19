# dejavu-integrate — Pipeline Skill

Wire [Deja Vu](https://dejavu.ai) into an existing repository end-to-end, using a goal-driven, test-first pipeline.

> **This is a pipeline skill, not a reference skill.** Invoke it as `/dejavu-integrate` when you want your assistant to do the work of integrating Deja Vu into a target repo. For day-to-day SDK coding help, install [`dejavu`](../dejavu/SKILL.md) instead.
>
> **Part of the Deja Vu Skill Graph:**
> - Reference: [dejavu](../dejavu/SKILL.md) · [dejavu-cli](../dejavu-cli/SKILL.md) · [dejavu-vercel-ai-sdk](../dejavu-vercel-ai-sdk/SKILL.md)
> - Pipeline: **dejavu-integrate** (this skill) → [dejavu-test-integration](../dejavu-test-integration/SKILL.md)

## What This Skill Does

When invoked, your assistant will:

- **Detect** the target repo's language and stack automatically
- **Ask** whether to integrate with Deja Vu Platform (managed) or Deja Vu Open Source (self-hosted)
- **Write failing tests first** — no implementation until tests exist
- **Keep the integration additive and feature-flagged** — existing behavior stays byte-for-byte identical when the flag is unset
- **Produce a local feature branch** (`dejavu-integrate/...`) and a `.dejavu-integration/` directory of artifacts (`goal.md`, `plan.md`, `product.json`) consumed by the companion verification skill

## When to Use

Trigger phrases:

- "Integrate Deja Vu into this repo"
- "Add Deja Vu to my project"
- "Wire Deja Vu into `<repo>`"
- "How do I add memory to an existing project?"

Do **not** use this skill for general SDK usage (install [`dejavu`](../dejavu/SKILL.md)), terminal workflows (install [`dejavu-cli`](../dejavu-cli/SKILL.md)), or Vercel AI SDK integration (install [`dejavu-vercel-ai-sdk`](../dejavu-vercel-ai-sdk/SKILL.md)).

## Installation

### CLI (Claude Code, Codex, OpenCode, OpenClaw, or any tool that supports skills)

```bash
npx skills add https://github.com/dejavu-memory/dejavu --skill dejavu-integrate
```

For verification on the same branch, also install the companion skill:

```bash
npx skills add https://github.com/dejavu-memory/dejavu --skill dejavu-test-integration
```

### Claude.ai

1. Download this `skills/dejavu-integrate` folder as a ZIP
2. Go to **Settings > Capabilities > Skills**
3. Click **Upload skill** and select the ZIP

### Claude API (Skills API)

```bash
curl -X POST https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "dejavu-integrate", "source": "https://github.com/dejavu-memory/dejavu/tree/main/skills/dejavu-integrate"}'
```

### Prerequisites

- A Deja Vu Platform API key ([get one](https://app.dejavu.ai/dashboard/api-keys)) *or* a working OSS setup (LLM + vector store)
- Python 3.10+ or Node.js 18+ in the target repo
- A clean working tree on the target repo's default branch

## Workflow

```
/dejavu-integrate          →  creates dejavu-integrate/<slug> branch,
                            writes .dejavu-integration/ artifacts,
                            implements against failing tests
/dejavu-test-integration   →  runs the repo's native test suite,
                            executes a real end-to-end smoke flow,
                            produces a scorecard
```

The two skills are loosely coupled — they share the same workspace and branch via `.dejavu-integration/`, but the verifier never modifies source.

## Links

- [Deja Vu Platform Dashboard](https://app.dejavu.ai)
- [Deja Vu Documentation](https://docs.dejavu.ai)
- [Deja Vu GitHub](https://github.com/dejavu-memory/dejavu)
- [Platform vs OSS comparison](https://docs.dejavu.ai/platform/platform-vs-oss)

## License

Apache-2.0
