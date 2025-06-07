# %% [markdown]
# api key setup for GROQ AND TAVILY

# %%
from dotenv import load_dotenv
load_dotenv()


import os
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY",'key not found')
GROQ_API_KEY = os.getenv("GROQ_API_KEY","key not found")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "key not found")
print("OPENAI_API_KEY:", OPENAI_API_KEY)
print("TAVILY_API_KEY:", TAVILY_API_KEY)
print("GROQ_API_KEY:", GROQ_API_KEY)

# %% [markdown]
# Importing libraries

# %%
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages.ai import AIMessage

# %% [markdown]
# LLM SETUP

# %%
openai_llm = ChatOpenAI(model="gpt-40-min")
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")

# %%
search_tool=TavilySearchResults(
    max_results=5
)

# %% [markdown]
# Setup Agent With Search Ability

# %%
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=groq_llm,
    tools=[search_tool],
    prompt="You are a helpful AI assistant that can search the web for information."
)

# %%
query = "tell me about the trends in krypto market"

# %%
state={"messages":query}
response=agent.invoke(state)
messages=response.get("messages",[])
messages

# %%
ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
print(ai_messages)
print(ai_messages[-1])

# %% [markdown]
# define the function

# %%
def get_response_from_ai_agent(llm_id,query,allow_search,prompt,provider):
    if provider == "groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "openai":
        llm = ChatOpenAI(model=llm_id)

    tools=[TavilySearchResults(max_results=5)] if allow_search else []    
       
    agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=prompt
    )

    state={"messages":query}
    response=agent.invoke(state)
    messages=response.get("messages",[])
    ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1] if ai_messages else "No response from AI agent."



