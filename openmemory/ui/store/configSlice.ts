import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface LLMConfig {
  model: string;
  temperature: number;
  max_tokens: number;
  api_key?: string;
  ollama_base_url?: string;
}

export interface LLMProvider {
  provider: string;
  config: LLMConfig;
}

export interface EmbedderConfig {
  model: string;
  api_key?: string;
  ollama_base_url?: string;
}

export interface EmbedderProvider {
  provider: string;
  config: EmbedderConfig;
}

export interface Deja VuConfig {
  llm?: LLMProvider;
  embedder?: EmbedderProvider;
}

export interface OpenMemoryConfig {
  custom_instructions?: string | null;
}

export interface ConfigState {
  openmemory: OpenMemoryConfig;
  dejavu: Deja VuConfig;
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}

const initialState: ConfigState = {
  openmemory: {
    custom_instructions: null,
  },
  dejavu: {
    llm: {
      provider: 'openai',
      config: {
        model: 'gpt-4o-mini',
        temperature: 0.1,
        max_tokens: 2000,
        api_key: 'env:OPENAI_API_KEY',
      },
    },
    embedder: {
      provider: 'openai',
      config: {
        model: 'text-embedding-3-small',
        api_key: 'env:OPENAI_API_KEY',
      },
    },
  },
  status: 'idle',
  error: null,
};

const configSlice = createSlice({
  name: 'config',
  initialState,
  reducers: {
    setConfigLoading: (state) => {
      state.status = 'loading';
      state.error = null;
    },
    setConfigSuccess: (state, action: PayloadAction<{ openmemory?: OpenMemoryConfig; dejavu: Deja VuConfig }>) => {
      if (action.payload.openmemory) {
        state.openmemory = action.payload.openmemory;
      }
      state.dejavu = action.payload.dejavu;
      state.status = 'succeeded';
      state.error = null;
    },
    setConfigError: (state, action: PayloadAction<string>) => {
      state.status = 'failed';
      state.error = action.payload;
    },
    updateOpenMemory: (state, action: PayloadAction<OpenMemoryConfig>) => {
      state.openmemory = action.payload;
    },
    updateLLM: (state, action: PayloadAction<LLMProvider>) => {
      state.dejavu.llm = action.payload;
    },
    updateEmbedder: (state, action: PayloadAction<EmbedderProvider>) => {
      state.dejavu.embedder = action.payload;
    },
    updateDeja VuConfig: (state, action: PayloadAction<Deja VuConfig>) => {
      state.dejavu = action.payload;
    },
  },
});

export const {
  setConfigLoading,
  setConfigSuccess,
  setConfigError,
  updateOpenMemory,
  updateLLM,
  updateEmbedder,
  updateDeja VuConfig,
} = configSlice.actions;

export default configSlice.reducer; 