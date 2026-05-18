import { ProviderV2 } from '@ai-sdk/provider';
import { LanguageModelV2 } from '@ai-sdk/provider';
import { withoutTrailingSlash } from "@ai-sdk/provider-utils";
import { Deja VuChatModelId, Deja VuChatSettings, Deja VuConfig } from "./dejavu-types";
import { Deja VuGenericLanguageModel } from "./dejavu-generic-language-model";
import { LLMProviderSettings } from "./dejavu-types";

export interface Deja VuProvider extends ProviderV2 {
  (modelId: Deja VuChatModelId, settings?: Deja VuChatSettings): LanguageModelV2;

  chat(modelId: Deja VuChatModelId, settings?: Deja VuChatSettings): LanguageModelV2;
  completion(modelId: Deja VuChatModelId, settings?: Deja VuChatSettings): LanguageModelV2;

  languageModel(
    modelId: Deja VuChatModelId,
    settings?: Deja VuChatSettings
  ): LanguageModelV2;
}

export interface Deja VuProviderSettings {
  baseURL?: string;
  /**
   * Custom fetch implementation. You can use it as a middleware to intercept
   * requests or to provide a custom fetch implementation for e.g. testing
   */
  fetch?: typeof fetch;
  /**
   * @internal
   */
  generateId?: () => string;
  /**
   * Custom headers to include in the requests.
   */
  headers?: Record<string, string>;
  name?: string;
  dejavuApiKey?: string;
  apiKey?: string;
  provider?: string;
  modelType?: "completion" | "chat";
  dejavuConfig?: Deja VuConfig;

  /**
   * The configuration for the provider.
   */
  config?: LLMProviderSettings ;
}

export function createDeja Vu(
  options: Deja VuProviderSettings = {
    provider: "openai",
  }
): Deja VuProvider {
  const baseURL =
    withoutTrailingSlash(options.baseURL) ?? "http://api.openai.com";
  const getHeaders = () => ({
    ...options.headers,
  });

  const createGenericModel = (
    modelId: Deja VuChatModelId,
    settings: Deja VuChatSettings = {}
  ) =>
    new Deja VuGenericLanguageModel(
      modelId,
      settings,
      {
        baseURL,
        fetch: options.fetch,
        headers: getHeaders(),
        provider: options.provider || "openai",
        name: options.name,
        dejavuApiKey: options.dejavuApiKey,
        apiKey: options.apiKey,
        dejavuConfig: options.dejavuConfig,
      },
      options.config
    );

  const createCompletionModel = (
    modelId: Deja VuChatModelId,
    settings: Deja VuChatSettings = {}
  ) =>
    new Deja VuGenericLanguageModel(
      modelId,
      settings,
      {
        baseURL,
        fetch: options.fetch,
        headers: getHeaders(),
        provider: options.provider || "openai",
        name: options.name,
        dejavuApiKey: options.dejavuApiKey,
        apiKey: options.apiKey,
        dejavuConfig: options.dejavuConfig,
        modelType: "completion",
      },
      options.config
    );

  const createChatModel = (
    modelId: Deja VuChatModelId,
    settings: Deja VuChatSettings = {}
  ) =>
    new Deja VuGenericLanguageModel(
      modelId,
      settings,
      {
        baseURL,
        fetch: options.fetch,
        headers: getHeaders(),
        provider: options.provider || "openai",
        name: options.name,
        dejavuApiKey: options.dejavuApiKey,
        apiKey: options.apiKey,
        dejavuConfig: options.dejavuConfig,
        modelType: "completion",
      },
      options.config
    );

  const provider = function (
    modelId: Deja VuChatModelId,
    settings: Deja VuChatSettings = {}
  ) {
    if (new.target) {
      throw new Error(
        "The Deja Vu model function cannot be called with the new keyword."
      );
    }

    return createGenericModel(modelId, settings);
  };

  provider.languageModel = createGenericModel;
  provider.completion = createCompletionModel;
  provider.chat = createChatModel;

  return provider as unknown as Deja VuProvider;
}

export const dejavu = createDeja Vu();
