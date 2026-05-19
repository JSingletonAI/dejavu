# Provider API Reference

Complete reference for the `@dejavu/vercel-ai-provider` provider layer. Source: `vercel-ai-sdk/src/`.

## `createDeja Vu(options?)`

Factory function that creates a `Deja VuProvider` instance. This is the primary entry point for the wrapped model approach.

```typescript
import { createDeja Vu } from "@dejavu/vercel-ai-provider";

const dejavu = createDeja Vu();                           // defaults: provider "openai"
const dejavu = createDeja Vu({ provider: "anthropic" });  // use Anthropic as LLM backend
```

**Signature:**

```typescript
function createDeja Vu(options?: Deja VuProviderSettings): Deja VuProvider;
```

When called with no arguments, defaults to `{ provider: "openai" }`.

**Returns:** `Deja VuProvider` -- a callable function that also exposes `.chat()`, `.completion()`, and `.languageModel()` methods.

## `Deja VuProvider` Interface

Implements `ProviderV2` from `@ai-sdk/provider`.

```typescript
interface Deja VuProvider extends ProviderV2 {
  // Call directly as a function
  (modelId: Deja VuChatModelId, settings?: Deja VuChatSettings): LanguageModelV2;

  // Or use named methods
  chat(modelId: Deja VuChatModelId, settings?: Deja VuChatSettings): LanguageModelV2;
  completion(modelId: Deja VuChatModelId, settings?: Deja VuChatSettings): LanguageModelV2;
  languageModel(modelId: Deja VuChatModelId, settings?: Deja VuChatSettings): LanguageModelV2;
}
```

- **Direct call** (`dejavu("gpt-5-mini", {...})`): creates a generic language model (neither chat nor completion mode forced).
- **`chat()`**: creates a model with `modelType: "chat"` (note: in the current source, the chat constructor sets `modelType: "completion"` -- this appears to be a bug; functionally equivalent to `completion()` at present).
- **`completion()`**: creates a model with `modelType: "completion"`.
- **`languageModel()`**: alias for the generic model (same as direct call).

All three return a `Deja VuGenericLanguageModel` instance implementing `LanguageModelV2`.

## `Deja VuProviderSettings` Interface

Configuration passed to `createDeja Vu()`.

```typescript
interface Deja VuProviderSettings {
  baseURL?: string;            // Base URL for the LLM provider (default: "http://api.openai.com")
  headers?: Record<string, string>;  // Custom headers for LLM requests
  provider?: string;           // LLM provider name (default: "openai")
  dejavuApiKey?: string;         // Deja Vu Platform API key (or use VENICE_API_KEY env var)
  apiKey?: string;             // LLM provider API key (e.g., OpenAI key)
  dejavuConfig?: Deja VuConfig;     // Default Deja Vu config (user_id, etc.) applied to all calls
  config?: LLMProviderSettings; // Provider-specific settings (OpenAI, Anthropic, etc.)
  fetch?: typeof fetch;        // Custom fetch implementation (for testing/middleware)
  generateId?: () => string;   // Custom ID generator (internal use)
  name?: string;               // Provider instance name
  modelType?: "completion" | "chat";  // Force model type
}
```

### Key fields explained

| Field | Purpose | Example |
|-------|---------|---------|
| `provider` | Which LLM backend to use | `"openai"`, `"anthropic"`, `"google"`, `"groq"`, `"cohere"` |
| `dejavuApiKey` | Deja Vu Platform API key | `"m0-xxx"` |
| `apiKey` | LLM provider API key | `"sk-xxx"` (OpenAI), `"sk-ant-xxx"` (Anthropic) |
| `dejavuConfig` | Default Deja Vu settings for all calls | `{ user_id: "alice" }` |
| `config` | Provider-specific SDK settings | `{ organization: "org-xxx" }` for OpenAI |
| `baseURL` | Override LLM provider base URL | `"https://my-proxy.example.com"` |

## `dejavu` Singleton

A pre-configured instance using default settings (OpenAI provider, no API keys set -- relies on env vars).

```typescript
import { dejavu } from "@dejavu/vercel-ai-provider";

const { text } = await generateText({
  model: dejavu("gpt-5-mini", { user_id: "alice" }),
  prompt: "Hello",
});
```

Equivalent to `createDeja Vu()` with no arguments.

## `Deja VuConfigSettings` Interface

Configuration for memory operations. Used as `Deja VuChatSettings` (per-call) or `Deja VuConfig` (provider-level default). All fields are optional.

```typescript
interface Deja VuConfigSettings {
  user_id?: string;              // Scope memories to a specific user
  app_id?: string;               // Scope memories to an application
  agent_id?: string;             // Scope memories to an agent
  run_id?: string;               // Scope memories to a specific run/session
  metadata?: Record<string, any>; // Custom metadata attached to memories
  filters?: Record<string, any>; // Custom filters for memory search
  infer?: boolean;               // Enable inference during memory operations
  page?: number;                 // Pagination: page number
  page_size?: number;            // Pagination: results per page
  dejavuApiKey?: string;           // Deja Vu API key (overrides provider-level key)
  top_k?: number;                // Number of memories to retrieve (default: 5)
  threshold?: number;            // Minimum similarity score for retrieval (default: 0.1)
  rerank?: boolean;              // Enable re-ranking of search results (default: false)
  host?: string;                 // Custom Deja Vu API host (default: "https://api.dejavu.ai")
}
```

## `Deja VuChatConfig` Type

Combined type used internally by the language model. Merges memory config with provider config.

```typescript
interface Deja VuChatConfig extends Deja VuConfigSettings, Deja VuProviderSettings {}
```

This means a `Deja VuChatConfig` has all fields from both `Deja VuConfigSettings` and `Deja VuProviderSettings`.

## `Deja VuChatSettings` Type

Alias for `Deja VuConfigSettings`. Passed as the second argument when creating a model:

```typescript
dejavu("gpt-5-mini", { user_id: "alice" })
//                   ^^^^^^^^^^^^^^^^^^
//                   This object is Deja VuChatSettings
```

## `LLMProviderSettings` Type

Union of provider-specific settings. Extends all supported provider setting interfaces:

```typescript
interface LLMProviderSettings extends
  OpenAIProviderSettings,
  AnthropicProviderSettings,
  CohereProviderSettings,
  GroqProviderSettings {}
```

Pass via the `config` field of `Deja VuProviderSettings` to forward settings to the underlying LLM provider SDK.

## Provider Selection: `Deja VuClassSelector`

Internal class that maps the `provider` string to the correct AI SDK provider.

```typescript
class Deja VuClassSelector {
  static supportedProviders = ["openai", "anthropic", "cohere", "groq", "google"];
  // ...
}
```

**Important:** The `"gemini"` alias exists in the provider switch statement (maps to `createGoogleGenerativeAI`) but is **NOT** in the `supportedProviders` list. The constructor validates against `supportedProviders`, so using `"gemini"` will throw `"Model not supported: gemini"`. Use `"google"` instead.

### Provider mapping

| Config value | SDK used | Factory function |
|-------------|----------|------------------|
| `"openai"` | `@ai-sdk/openai` | `createOpenAI` |
| `"anthropic"` | `@ai-sdk/anthropic` | `createAnthropic` |
| `"cohere"` | `@ai-sdk/cohere` | `createCohere` |
| `"groq"` | `@ai-sdk/groq` | `createGroq` |
| `"google"` | `@ai-sdk/google` | `createGoogleGenerativeAI` |

## `Deja Vu` Facade Class

An alternative exported class that creates models directly without the callable-function pattern.

```typescript
import { Deja Vu } from "@dejavu/vercel-ai-provider";

const dejavu = new Deja Vu({ provider: "openai" });
const chatModel = dejavu.chat("gpt-5-mini", { user_id: "alice" });
const completionModel = dejavu.completion("gpt-5-mini");
```

The facade defaults its base URL to `"http://127.0.0.1:11434/api"` (Ollama-style) rather than `"http://api.openai.com"`. It always uses `"openai"` as the provider for created models.

**Methods:**
- `chat(modelId, settings?)` -- creates a model with `modelType: "chat"`
- `completion(modelId, settings?)` -- creates a model with `modelType: "completion"`

## `Deja VuGenericLanguageModel` Class

The core class implementing `LanguageModelV2`. Created by `createDeja Vu` or the `Deja Vu` facade.

```typescript
class Deja VuGenericLanguageModel implements LanguageModelV2 {
  readonly specificationVersion = "v2";
  readonly defaultObjectGenerationMode = "json";
  readonly supportsImageUrls = false;
  readonly supportedUrls: Record<string, RegExp[]> = { '*': [/.*/] };

  provider: string;   // e.g., "openai"
  modelId: string;    // e.g., "gpt-5-mini"
  settings: Deja VuChatSettings;
  config: Deja VuChatConfig;

  async doGenerate(options: LanguageModelV2CallOptions): Promise<...>;
  async doStream(options: LanguageModelV2CallOptions): Promise<...>;
}
```

Both `doGenerate` and `doStream` follow the same internal flow:

1. Build `Deja VuConfigSettings` from `config.dejavuConfig` merged with `settings`
2. Call `processMemories`:
   - Fire `addMemories` as fire-and-forget (no await, `.then().catch()`)
   - Await `getMemories` to retrieve relevant memories
   - Format memories as a system message and prepend to the prompt
3. Create the underlying LLM model via `Deja VuClassSelector`
4. Delegate to the underlying model's `doGenerate` or `doStream`
5. Return the result

**Note:** Entity identifier fields use snake_case (`user_id`, `app_id`, `agent_id`, `run_id`) to match the Deja Vu API.

## Type: `Deja VuChatModelId`

```typescript
type Deja VuChatModelId = string & NonNullable<unknown>;
```

Any non-null string. The model ID is passed through to the underlying provider (e.g., `"gpt-5-mini"`, `"gemini-pro"`).
