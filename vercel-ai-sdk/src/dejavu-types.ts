import { Deja VuProviderSettings } from "./dejavu-provider";
import { OpenAIProviderSettings } from "@ai-sdk/openai";
import { AnthropicProviderSettings } from "@ai-sdk/anthropic";
import { LanguageModelV2 } from '@ai-sdk/provider';
import { CohereProviderSettings } from "@ai-sdk/cohere";
import { GroqProviderSettings } from "@ai-sdk/groq";
export type Deja VuChatModelId =
  | (string & NonNullable<unknown>);

export interface Deja VuConfigSettings {
  user_id?: string;
  app_id?: string;
  agent_id?: string;
  run_id?: string;
  org_name?: string;
  project_name?: string;
  org_id?: string;
  project_id?: string;
  metadata?: Record<string, any>;
  filters?: Record<string, any>;
  infer?: boolean;
  page?: number;
  page_size?: number;
  dejavuApiKey?: string;
  top_k?: number;
  threshold?: number;
  rerank?: boolean;
  enable_graph?: boolean;
  host?: string;
  output_format?: string;
  filter_memories?: boolean;
  async_mode?: boolean;
}

export interface Deja VuChatConfig extends Deja VuConfigSettings, Deja VuProviderSettings {}

export interface LLMProviderSettings extends OpenAIProviderSettings, AnthropicProviderSettings, CohereProviderSettings, GroqProviderSettings {}

export interface Deja VuConfig extends Deja VuConfigSettings {}
export interface Deja VuChatSettings extends Deja VuConfigSettings {}

export interface Deja VuStreamResponse extends Awaited<ReturnType<LanguageModelV2['doStream']>> {
  memories: any;
}
