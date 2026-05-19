# dejavu-test-integration — Pipeline Skill

Verify a Deja Vu integration produced by [`/dejavu-integrate`](../dejavu-integrate/SKILL.md). Runs in the same workspace on the same branch — installs dependencies, runs the repo's native test suite, then exercises a real end-to-end smoke flow against the user's API key.

> **This is a pipeline skill, not a reference skill.** Invoke it as `/dejavu-test-integration` after `/dejavu-integrate` has produced a branch to verify. It catches compile and runtime bugs by design — logical integration errors (wrong data stored, wrong scoping) are for human review.
>
> **Part of the Deja Vu Skill Graph:**
> - Reference: [dejavu](../dejavu/SKILL.md) · [dejavu-cli](../dejavu-cli/SKILL.md) · [dejavu-vercel-ai-sdk](../dejavu-vercel-ai-sdk/SKILL.md)
> - Pipeline: [dejavu-integrate](../dejavu-integrate/SKILL.md) → **dejavu-test-integration** (this skill)

## What This Skill Does

When invoked, your assistant will:

- **Refuse to start** unless the branch has `.dejavu-integration/` artifacts, the working tree is clean, and the right API key is in the environment
- **Install** the repo's dependencies using its native tooling (pip, pnpm, npm, hatch, etc.)
- **Run the native test suite** in two passes: flag-unset (must behave like `main`) and flag-set (new tests run)
- **Execute a real end-to-end smoke flow** against Deja Vu Platform (`VENICE_API_KEY`) or OSS (`OPENAI_API_KEY`)
- **Produce a scorecard** — `overall: pass | fail`, per-check reasons, and the reproduction command for each failure

## When to Use

Trigger phrases:

- "Verify the integration"
- "Test the Deja Vu integration"
- "Run `/dejavu-test-integration`"

Do **not** use this skill to run general project tests (defer to the repo's native test command) or before `/dejavu-integrate` has produced a branch on the current workspace.

## Installation

### CLI (Claude Code, Codex, OpenCode, OpenClaw, or any tool that supports skills)

```bash
npx skills add https://github.com/dejavu-memory/dejavu --skill dejavu-test-integration
```

Typically installed alongside the companion pipeline skill:

```bash
npx skills add https://github.com/dejavu-memory/dejavu --skill dejavu-integrate
```

### Claude.ai

1. Download this `skills/dejavu-test-integration` folder as a ZIP
2. Go to **Settings > Capabilities > Skills**
3. Click **Upload skill** and select the ZIP

### Claude API (Skills API)

```bash
curl -X POST https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "dejavu-test-integration", "source": "https://github.com/dejavu-memory/dejavu/tree/main/skills/dejavu-test-integration"}'
```

### Preconditions

The skill refuses to start unless all of the following are true:

- `.dejavu-integration/` directory exists in the repo root
- Current branch starts with `dejavu-integrate/`
- Working tree is clean
- The same API key used during `/dejavu-integrate` is exported in the environment

## What This Skill Does *Not* Catch

By design, this skill only catches compile and runtime bugs. Logical errors — memories stored with the wrong scoping, retrieval returning the wrong user's data, filter mismatches — are the human reviewer's responsibility.

## Links

- [Deja Vu Documentation](https://docs.dejavu.ai)
- [Deja Vu GitHub](https://github.com/dejavu-memory/dejavu)
- [API Reference](https://docs.dejavu.ai/api-reference)

## License

Apache-2.0
