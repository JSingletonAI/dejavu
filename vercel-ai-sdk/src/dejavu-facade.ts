import { withoutTrailingSlash } from '@ai-sdk/provider-utils'

import { Deja VuGenericLanguageModel } from './dejavu-generic-language-model'
import { Deja VuChatModelId, Deja VuChatSettings } from './dejavu-types'
import { Deja VuProviderSettings } from './dejavu-provider'

export class Deja Vu {
  readonly baseURL: string
  readonly headers?: any

  constructor(options: Deja VuProviderSettings = {
    provider: 'openai',
  }) {
    this.baseURL =
      withoutTrailingSlash(options.baseURL) ?? 'http://127.0.0.1:11434/api'

    this.headers = options.headers
  }

  private get baseConfig() {
    return {
      baseURL: this.baseURL,
      headers: this.headers,
    }
  }

  chat(modelId: Deja VuChatModelId, settings: Deja VuChatSettings = {}) {
    return new Deja VuGenericLanguageModel(modelId, settings, {
      provider: 'openai',
      modelType: 'chat',
      ...this.baseConfig,
    })
  }

  completion(modelId: Deja VuChatModelId, settings: Deja VuChatSettings = {}) {
    return new Deja VuGenericLanguageModel(modelId, settings, {
      provider: 'openai',
      modelType: 'completion',
      ...this.baseConfig,
    })
  }
}