import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from tools import find_route, calculate_fare, get_station_info
import streamlit as st

load_dotenv()

# Read API key — from Streamlit Cloud secrets OR .env file
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

# Groq Model
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    api_key=api_key
)

# Load Vector Store (metro knowledge base)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Tools
tools = [find_route, calculate_fare, get_station_info]
llm_with_tools = llm.bind_tools(tools)

def get_response(user_input: str):
    try:
        # 1. Retrieve relevant information from data
        docs = retriever.invoke(user_input)
        context = "\n\n".join([doc.page_content for doc in docs])

        # 2. Build system prompt
        system_prompt = f"""You are Metro Buddy 🚇 — a friendly, fun and helpful assistant for Surat Smart Metro.

You have two modes:
1. **Metro Expert**: Answer questions about routes, fares, stations, timings using the data below.
2. **Friendly Companion**: If someone greets you, chats casually, asks how you are, or says something funny — respond warmly and naturally like a helpful friend would. Keep it short and light.

Metro Knowledge Base:
{context}

Personality Rules:
- Be warm, friendly and a little fun — not robotic
- Use emojis occasionally (don't overdo it)
- For greetings like "hi", "hello", "how are you" — respond casually and invite them to ask about metro
- For small talk — engage briefly then gently guide back to metro topics
- For metro questions — be accurate, clear and helpful
- If asked something you don't know — say "Hmm, I'm not sure about that one! But I can definitely help you with Surat Metro routes, fares and stations 😊"
- Keep responses concise — no long paragraphs unless needed
- Never make up metro data — only use the provided context and tool outputs
"""

        messages = [
            ("system", system_prompt),
            ("human", user_input)
        ]

        response = llm_with_tools.invoke(messages)

        # If a tool call was triggered
        if hasattr(response, "tool_calls") and response.tool_calls:
            tool_outputs = []

            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                if tool_name == "find_route":
                    result = find_route.invoke(tool_args)
                elif tool_name == "calculate_fare":
                    result = calculate_fare.invoke(tool_args)
                elif tool_name == "get_station_info":
                    result = get_station_info.invoke(tool_args)
                else:
                    result = "Tool not found"

                tool_outputs.append(f"{tool_name} → {result}")

            final_prompt = f"""User asked: {user_input}

Tool information:
{chr(10).join(tool_outputs)}

Context from data:
{context}

Based on this information, provide a helpful and clear response in English."""

            final_response = llm.invoke(final_prompt)
            return final_response.content

        return response.content

    except Exception as e:
        return f"Error: {str(e)}"