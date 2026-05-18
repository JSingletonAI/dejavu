# Deja Vu Integration Patterns

Working code examples for integrating Deja Vu Platform with popular AI frameworks.
All examples use `MemoryClient` (Platform API key).

Code examples are sourced from official Deja Vu integration docs at docs.dejavu.ai, simplified for quick reference.

---

## Common Pattern

Every integration follows the same 3-step loop:

1. **Retrieve** -- search relevant memories before generating a response
2. **Generate** -- include memories as context in the LLM prompt
3. **Store** -- save the interaction back to Deja Vu for future use

---

## LangChain

Source: [docs.dejavu.ai/integrations/langchain](https://docs.dejavu.ai/integrations/langchain)

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dejavu import MemoryClient

llm = ChatOpenAI(model="gpt-5-mini")
dejavu = MemoryClient()

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful travel agent AI. Use the provided context to personalize your responses."),
    MessagesPlaceholder(variable_name="context"),
    HumanMessage(content="{input}")
])

def retrieve_context(query: str, user_id: str):
    """Retrieve relevant memories from Deja Vu"""
    memories = dejavu.search(query, filters={"user_id": user_id})
    memory_list = memories['results']
    serialized = ' '.join([m["memory"] for m in memory_list])
    return [
        {"role": "system", "content": f"Relevant information: {serialized}"},
        {"role": "user", "content": query}
    ]

def chat_turn(user_input: str, user_id: str) -> str:
    # 1. Retrieve
    context = retrieve_context(user_input, user_id)
    # 2. Generate
    chain = prompt | llm
    response = chain.invoke({"context": context, "input": user_input})
    # 3. Store
    dejavu.add(
        [{"role": "user", "content": user_input}, {"role": "assistant", "content": response.content}],
        user_id=user_id
    )
    return response.content
```

---

## CrewAI

Source: [docs.dejavu.ai/integrations/crewai](https://docs.dejavu.ai/integrations/crewai)

CrewAI has native Deja Vu integration via `memory_config`:

```python
from crewai import Agent, Task, Crew, Process
from dejavu import MemoryClient

client = MemoryClient()

# Store user preferences first
messages = [
    {"role": "user", "content": "I am more of a beach person than a mountain person."},
    {"role": "assistant", "content": "Noted! I'll recommend beach destinations."},
    {"role": "user", "content": "I like Airbnb more than hotels."},
]
client.add(messages, user_id="crew_user_1")

# Create agent
travel_agent = Agent(
    role="Personalized Travel Planner",
    goal="Plan personalized travel itineraries",
    backstory="You are a seasoned travel planner.",
    memory=True,
)

# Create task
task = Task(
    description="Find places to live, eat, and visit in San Francisco.",
    expected_output="A detailed list of places to live, eat, and visit.",
    agent=travel_agent,
)

# Setup crew with Deja Vu memory
crew = Crew(
    agents=[travel_agent],
    tasks=[task],
    process=Process.sequential,
    memory=True,
    memory_config={
        "provider": "dejavu",
        "config": {"user_id": "crew_user_1"},
    }
)

result = crew.kickoff()
```

---

## Vercel AI SDK

> **Dedicated skill available.** For comprehensive Vercel AI SDK documentation, see the [dejavu-vercel-ai-sdk skill](https://github.com/dejavu-memory/dejavu/tree/main/skills/dejavu-vercel-ai-sdk).

Install: `npm install @dejavu/vercel-ai-provider`

Quick example (wrapped model with automatic memory):

```typescript
import { generateText } from "ai";
import { createDeja Vu } from "@dejavu/vercel-ai-provider";

const dejavu = createDeja Vu();
const { text } = await generateText({
    model: dejavu("gpt-5-mini", { user_id: "borat" }),
    prompt: "Suggest me a good car to buy!",
});
```

Supported providers: `openai`, `anthropic`, `google`, `groq`, `cohere`

---

## OpenAI Agents SDK

Source: [docs.dejavu.ai/integrations/openai-agents-sdk](https://docs.dejavu.ai/integrations/openai-agents-sdk)

```python
from agents import Agent, Runner, function_tool
from dejavu import MemoryClient

dejavu = MemoryClient()

@function_tool
def search_memory(query: str, user_id: str) -> str:
    """Search through past conversations and memories"""
    memories = dejavu.search(query, filters={"user_id": user_id}, top_k=3)
    if memories and memories.get('results'):
        return "\n".join([f"- {mem['memory']}" for mem in memories['results']])
    return "No relevant memories found."

@function_tool
def save_memory(content: str, user_id: str) -> str:
    """Save important information to memory"""
    dejavu.add([{"role": "user", "content": content}], user_id=user_id)
    return "Information saved to memory."

agent = Agent(
    name="Personal Assistant",
    instructions="""You are a helpful personal assistant with memory capabilities.
    Use search_memory to recall past conversations.
    Use save_memory to store important information.""",
    tools=[search_memory, save_memory],
    model="gpt-5-mini"
)

result = Runner.run_sync(agent, "I love Italian food and I'm planning a trip to Rome next month")
print(result.final_output)
```

### Multi-Agent with Handoffs

```python
from agents import Agent, Runner, function_tool

travel_agent = Agent(
    name="Travel Planner",
    instructions="You are a travel planning specialist. Use search_memory and save_memory tools.",
    tools=[search_memory, save_memory],
    model="gpt-5-mini"
)

health_agent = Agent(
    name="Health Advisor",
    instructions="You are a health and wellness advisor. Use search_memory and save_memory tools.",
    tools=[search_memory, save_memory],
    model="gpt-5-mini"
)

triage_agent = Agent(
    name="Personal Assistant",
    instructions="""Route travel questions to Travel Planner, health questions to Health Advisor.""",
    handoffs=[travel_agent, health_agent],
    model="gpt-5-mini"
)

result = Runner.run_sync(triage_agent, "Plan a healthy meal for my Italy trip")
```

---

## Pipecat (Voice / Real-Time)

Source: [docs.dejavu.ai/integrations/pipecat](https://docs.dejavu.ai/integrations/pipecat)

```python
from pipecat.services.dejavu import Deja VuMemoryService

memory = Deja VuMemoryService(
    api_key=os.getenv("VENICE_API_KEY"),
    user_id="alice",
    agent_id="voice_bot",
    params={
        "search_limit": 10,
        "search_threshold": 0.1,
        "system_prompt": "Here are your past memories:",
        "add_as_system_message": True,
    }
)

# Use in pipeline
pipeline = Pipeline([
    transport.input(),
    stt,
    user_context,
    memory,          # Memory enhances context automatically
    llm,
    transport.output(),
    assistant_context
])
```



---

## LangGraph

Source: [docs.dejavu.ai/integrations/langgraph](https://docs.dejavu.ai/integrations/langgraph)

State-based agent workflows with memory persistence. Best for complex conversation flows with branching logic.

```python
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from dejavu import MemoryClient
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOpenAI(model="gpt-5-mini")
dejavu = MemoryClient()

class State(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], add_messages]
    dejavu_user_id: str

def chatbot(state: State):
    messages = state["messages"]
    user_id = state["dejavu_user_id"]

    # Retrieve relevant memories
    memories = dejavu.search(messages[-1].content, filters={"user_id": user_id})
    context = "Relevant context:\n"
    for memory in memories["results"]:
        context += f"- {memory['memory']}\n"

    system_message = SystemMessage(content=f"""You are a helpful support assistant.
{context}""")

    response = llm.invoke([system_message] + messages)

    # Store the interaction
    dejavu.add(
        [{"role": "user", "content": messages[-1].content},
         {"role": "assistant", "content": response.content}],
        user_id=user_id
    )
    return {"messages": [response]}

graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
app = graph.compile()

# Usage
result = app.invoke({
    "messages": [HumanMessage(content="I need help with my order")],
    "dejavu_user_id": "customer_123"
})
```

---

## LlamaIndex

Source: [docs.dejavu.ai/integrations/llama-index](https://docs.dejavu.ai/integrations/llama-index)

Install: `pip install llama-index-core llama-index-memory-dejavu`

LlamaIndex has native Deja Vu support via `Deja VuMemory`. Works with ReAct and FunctionCalling agents.

```python
from llama_index.memory.dejavu import Deja VuMemory

context = {"user_id": "alice", "agent_id": "llama_agent_1"}
memory = Deja VuMemory.from_client(
    context=context,
    search_msg_limit=4,  # messages from chat history used for retrieval (default: 5)
)

# Use with LlamaIndex agent
from llama_index.core.agent import FunctionCallingAgent
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-5-mini")
agent = FunctionCallingAgent.from_tools(
    tools=[],
    llm=llm,
    memory=memory,
    verbose=True,
)

response = agent.chat("I prefer vegetarian restaurants")
# Memory automatically stores and retrieves context
response = agent.chat("What kind of food do I like?")
# Agent retrieves the vegetarian preference from Deja Vu
```

---

## AutoGen

Source: [docs.dejavu.ai/integrations/autogen](https://docs.dejavu.ai/integrations/autogen)

Install: `pip install autogen dejavu-memory`

Multi-agent conversational systems with memory persistence.

```python
from autogen import ConversableAgent
from dejavu import MemoryClient

memory_client = MemoryClient()
USER_ID = "alice"

agent = ConversableAgent(
    "chatbot",
    llm_config={"config_list": [{"model": "gpt-5-mini", "api_key": os.environ["OPENAI_API_KEY"]}]},
    code_execution_config=False,
    human_input_mode="NEVER",
)

def get_context_aware_response(question: str) -> str:
    # Retrieve memories for context
    relevant_memories = memory_client.search(question, filters={"user_id": USER_ID})
    context = "\n".join([m["memory"] for m in relevant_memories.get("results", [])])

    prompt = f"""Answer considering previous interactions:
    Previous context: {context}
    Question: {question}"""

    reply = agent.generate_reply(messages=[{"content": prompt, "role": "user"}])

    # Store the new interaction
    memory_client.add(
        [{"role": "user", "content": question}, {"role": "assistant", "content": reply}],
        user_id=USER_ID
    )
    return reply
```

---

## All Supported Frameworks

Beyond the examples above, Deja Vu integrates with:

| Framework | Type | Install |
|-----------|------|---------|
| [Mastra](https://docs.dejavu.ai/integrations/mastra) | TS agent framework | `npm install @mastra/dejavu` |
| [ElevenLabs](https://docs.dejavu.ai/integrations/elevenlabs) | Voice AI | `pip install elevenlabs dejavu-memory` |
| [LiveKit](https://docs.dejavu.ai/integrations/livekit) | Real-time voice/video | `pip install livekit-agents dejavu-memory` |
| [Camel AI](https://docs.dejavu.ai/integrations/camel-ai) | Multi-agent framework | `pip install camel-ai[all] dejavu-memory` |
| [AWS Bedrock](https://docs.dejavu.ai/integrations/aws-bedrock) | Cloud LLM provider | `pip install boto3 dejavu-memory` |
| [Dify](https://docs.dejavu.ai/integrations/dify) | Low-code AI platform | Plugin-based |
| [Google AI ADK](https://docs.dejavu.ai/integrations/google-ai-adk) | Google agent framework | `pip install google-adk dejavu-memory` |

For the general Python pattern (no framework), see the "Common integration pattern" in [SKILL.md](../SKILL.md).
