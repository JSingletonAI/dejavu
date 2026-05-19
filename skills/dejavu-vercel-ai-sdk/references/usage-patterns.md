# Usage Patterns and Examples

Working examples for `@dejavu/vercel-ai-provider`. All examples assume environment variables `VENICE_API_KEY` and the relevant LLM provider API key are set.

## 1. Wrapped Model with generateText (Basic)

The simplest way to add memory to any LLM call.

```typescript
import { generateText } from "ai";
import { createDeja Vu } from "@dejavu/vercel-ai-provider";

const dejavu = createDeja Vu();

const { text } = await generateText({
  model: dejavu("gpt-5-mini", { user_id: "alice" }),
  prompt: "Recommend a restaurant based on my preferences",
});

console.log(text);
```

Memories are automatically retrieved before the call and stored after.

## 2. Wrapped Model with streamText (Streaming)

Stream responses with automatic memory augmentation.

```typescript
import { streamText } from "ai";
import { createDeja Vu } from "@dejavu/vercel-ai-provider";

const dejavu = createDeja Vu();

const result = streamText({
  model: dejavu("gpt-5-mini", { user_id: "alice" }),
  prompt: "What should I cook for dinner tonight?",
});

for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}
```

Memory retrieval happens before streaming begins. The conversation is stored to Deja Vu as a fire-and-forget call (non-blocking).

## 3. Standalone Utilities with OpenAI

Full control over the memory lifecycle using standalone functions with OpenAI.

```typescript
import { openai } from "@ai-sdk/openai";
import { generateText } from "ai";
import { retrieveMemories, addMemories } from "@dejavu/vercel-ai-provider";

const user_id = "alice";
const prompt = "Suggest a weekend trip";

// Step 1: Retrieve memories as a formatted system prompt
const memories = await retrieveMemories(prompt, {
  user_id: user_id,
});

// Step 2: Generate with the memories injected as system context
const { text } = await generateText({
  model: openai("gpt-5-mini"),
  prompt,
  system: memories,
});

console.log(text);

// Step 3: Store the conversation as new memories
await addMemories(
  [
    { role: "user", content: [{ type: "text", text: prompt }] },
    { role: "assistant", content: [{ type: "text", text }] },
  ],
  { user_id: user_id }
);
```

## 4. Standalone Utilities with Anthropic

Same pattern, different LLM provider.

```typescript
import { anthropic } from "@ai-sdk/anthropic";
import { generateText } from "ai";
import { retrieveMemories, addMemories } from "@dejavu/vercel-ai-provider";

const prompt = "Help me plan my exercise routine";
const config = { user_id: "bob" };

const memories = await retrieveMemories(prompt, config);

const { text } = await generateText({
  model: anthropic("claude-sonnet-4-20250514"),
  prompt,
  system: memories,
});

await addMemories(
  [
    { role: "user", content: [{ type: "text", text: prompt }] },
    { role: "assistant", content: [{ type: "text", text }] },
  ],
  config
);
```

## 5. Structured Output with generateObject

Use with `generateObject` for typed, structured responses enriched with memory.

```typescript
import { generateObject } from "ai";
import { createDeja Vu } from "@dejavu/vercel-ai-provider";
import { z } from "zod";

const dejavu = createDeja Vu();

const { object } = await generateObject({
  model: dejavu("gpt-5-mini", { user_id: "alice" }),
  prompt: "Suggest a meal plan for today",
  schema: z.object({
    breakfast: z.string(),
    lunch: z.string(),
    dinner: z.string(),
    snacks: z.array(z.string()),
    notes: z.string().describe("Personalization notes based on known preferences"),
  }),
});

console.log(object);
// { breakfast: "Avocado toast (you mentioned loving it)", lunch: "...", ... }
```

The `defaultObjectGenerationMode` is `"json"`, so structured output works out of the box.

## 6. Multi-Provider Setup

Configure different LLM providers with the wrapped model.

### OpenAI (default)

```typescript
import { createDeja Vu } from "@dejavu/vercel-ai-provider";

const dejavu = createDeja Vu(); // defaults to "openai"
const model = dejavu("gpt-5-mini", { user_id: "alice" });
```

### Anthropic

```typescript
const dejavu = createDeja Vu({ provider: "anthropic" });
const model = dejavu("claude-sonnet-4-20250514", { user_id: "alice" });
```

### Google

```typescript
const dejavu = createDeja Vu({ provider: "google" });
const model = dejavu("gemini-2.0-flash", { user_id: "alice" });
```

### Groq

```typescript
const dejavu = createDeja Vu({ provider: "groq" });
const model = dejavu("llama-3.3-70b-versatile", { user_id: "alice" });
```

### Cohere

```typescript
const dejavu = createDeja Vu({ provider: "cohere" });
const model = dejavu("command-r-plus", { user_id: "alice" });
```

### With explicit API keys (no env vars)

```typescript
const dejavu = createDeja Vu({
  provider: "openai",
  apiKey: "sk-xxx",       // OpenAI API key
  dejavuApiKey: "m0-xxx",   // Deja Vu API key
});
```

## 7. Next.js API Route Integration

A POST handler that uses the wrapped model in a Next.js App Router API route.

```typescript
// app/api/chat/route.ts
import { streamText } from "ai";
import { createDeja Vu } from "@dejavu/vercel-ai-provider";

const dejavu = createDeja Vu();

export async function POST(req: Request) {
  const { messages, user_id } = await req.json();

  const lastMessage = messages[messages.length - 1];

  const result = streamText({
    model: dejavu("gpt-5-mini", { user_id }),
    prompt: lastMessage.content,
  });

  return result.toDataStreamResponse();
}
```

### With standalone utilities for more control

```typescript
// app/api/chat/route.ts
import { openai } from "@ai-sdk/openai";
import { streamText } from "ai";
import { retrieveMemories, addMemories } from "@dejavu/vercel-ai-provider";

export async function POST(req: Request) {
  const { messages, user_id } = await req.json();
  const lastMessage = messages[messages.length - 1];

  // Retrieve relevant memories
  const memories = await retrieveMemories(lastMessage.content, {
    user_id,
  });

  // Stream the response
  const result = streamText({
    model: openai("gpt-5-mini"),
    prompt: lastMessage.content,
    system: memories,
  });

  // Store conversation in the background (fire-and-forget)
  result.text.then(async (text) => {
    await addMemories(
      [
        { role: "user", content: [{ type: "text", text: lastMessage.content }] },
        { role: "assistant", content: [{ type: "text", text }] },
      ],
      { user_id }
    );
  });

  return result.toDataStreamResponse();
}
```

## 8. How Memory Processing Works Internally

### Wrapped model flow (doGenerate / doStream)

```
1. doGenerate(options) or doStream(options) is called
2. processMemories(messagesPrompts, dejavuConfig):
   a. addMemories(messagesPrompts, dejavuConfig)
      --> fire-and-forget: .then().catch(), NO await
      --> POST /v3/memories/add/ with converted messages
   b. await getMemories(messagesPrompts, dejavuConfig)
      --> POST /v3/memories/search/ with flattened prompt
      --> returns memory array
   c. Format memories into system message string
   d. Prepend system message to messagesPrompts array
   e. Return { memories, messagesPrompts }
3. Create underlying LLM via Deja VuClassSelector.createProvider()
4. Call model.doGenerate(updatedOptions) or model.doStream(updatedOptions)
5. Return result
```

**Critical detail:** The `addMemories` call in step 2a is **NON-BLOCKING**. It uses `.then().catch()` without `await`, meaning:
- Memory storage happens asynchronously in the background
- The LLM response is not delayed by the memory write
- If the memory write fails, it logs an error but does not affect the response
- There is a brief window where the latest conversation is not yet stored

### Memory injection format

The memories are injected as a system message at position 0 of the prompt array:

```typescript
{
  role: "system",
  content: "System Message: These are the memories I have stored. Give more weightage to the question by users and try to answer that first. You have to modify your answer based on the memories I have provided. If the memories are irrelevant you can ignore them. Also don't reply to this section of the prompt, or the memories, they are only for your reference. The System prompt starts after text System Message: \n\n Memory: ... \n\n Memory: ... \n\n"
}
```

## 9. Custom Configuration

### Custom Deja Vu API host

```typescript
const dejavu = createDeja Vu({
  dejavuConfig: {
    host: "https://my-dejavu-instance.example.com",
  },
});
```

Or with standalone utilities:

```typescript
const memories = await retrieveMemories(prompt, {
  user_id: "alice",
  host: "https://my-dejavu-instance.example.com",
});
```

### Memory filtering and ranking

```typescript
const dejavu = createDeja Vu();
const model = dejavu("gpt-5-mini", {
  user_id: "alice",
  top_k: 10,          // retrieve up to 10 memories (default: 5)
  threshold: 0.8,     // only memories with score >= 0.8
  rerank: true,       // enable re-ranking of results
});
```

### Provider-specific configuration

Pass SDK-specific settings via the `config` field:

```typescript
const dejavu = createDeja Vu({
  provider: "openai",
  config: {
    organization: "org-xxx",
    project: "proj-xxx",
  },
});
```

### Default Deja Vu config for all calls

Set defaults at the provider level that apply to every model created:

```typescript
const dejavu = createDeja Vu({
  dejavuConfig: {
    user_id: "alice",
    top_k: 10,
  },
});

// These calls inherit user_id and top_k from dejavuConfig
const { text } = await generateText({
  model: dejavu("gpt-5-mini"),
  prompt: "Hello",
});
```

Per-call settings (passed as the second argument to `dejavu()`) are merged on top of `dejavuConfig`, so you can override specific fields:

```typescript
// Override user_id for this specific call
const model = dejavu("gpt-5-mini", { user_id: "bob" });
```

The merge order is: `config.dejavuConfig` (provider defaults) < `settings` (per-call overrides).
