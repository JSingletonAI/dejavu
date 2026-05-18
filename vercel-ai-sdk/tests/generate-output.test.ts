import { generateText, streamText } from "ai";
import { LanguageModelV2Prompt } from '@ai-sdk/provider';
import { simulateStreamingMiddleware, wrapLanguageModel } from 'ai';
import { addMemories } from "../src";
import { testConfig } from "../config/test-config";

interface Provider {
  name: string;
  activeModel: string;
  apiKey: string | undefined;
}

describe.each(testConfig.providers)('TESTS: Generate/Stream Text with model %s', (provider: Provider) => {
  const { userId } = testConfig;
  let dejavu: ReturnType<typeof testConfig.createTestClient>;
  jest.setTimeout(50000);
  
  beforeEach(() => {
    dejavu = testConfig.createTestClient(provider);
  });

  beforeAll(async () => {
    // Add some test memories before all tests
    const messages: LanguageModelV2Prompt = [
      {
        role: "user",
        content: [
          { type: "text", text: "I love red cars." },
          { type: "text", text: "I like Toyota Cars." },
          { type: "text", text: "I prefer SUVs." },
        ],
      }
    ];
    await addMemories(messages, { user_id: userId });
  });

  it("should generate text using dejavu model", async () => {
    const { text } = await generateText({
      model: dejavu(provider.activeModel, {
        user_id: userId,
      }),
      prompt: "Suggest me a good car to buy!",
    });

    expect(typeof text).toBe('string');
    expect(text.length).toBeGreaterThan(0);
  });

  it("should generate text using provider with memories", async () => {
    const { text } = await generateText({
      model: dejavu(provider.activeModel, {
        user_id: userId,
      }),
      messages: [
        {
          role: "user",
          content: [
            { type: "text", text: "Suggest me a good car to buy." },
            { type: "text", text: "Write only the car name and it's color." },
          ]
        }
      ],
    });
    // Expect text to be a string
    expect(typeof text).toBe('string');
    expect(text.length).toBeGreaterThan(0);
  });

  it("should stream text using Deja Vu provider with new streaming approach", async () => {
    // Create the base model
    const baseModel = dejavu(provider.activeModel, {
      user_id: userId,
    });

    // Wrap with streaming middleware using the new Vercel AI SDK 5.0 approach
    const model = wrapLanguageModel({
      model: baseModel,
      middleware: simulateStreamingMiddleware(),
    });

    const { textStream } = streamText({
      model,
      prompt: "Suggest me a good car to buy! Write only the car name and it's color.",
    });
  
    // Collect streamed text parts
    let streamedText = '';
    for await (const textPart of textStream) {
      streamedText += textPart;
    }
  
    // Ensure the streamed text is a string
    expect(typeof streamedText).toBe('string');
    expect(streamedText.length).toBeGreaterThan(0);
  });
  
});