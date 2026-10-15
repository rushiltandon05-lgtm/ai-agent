ai-agent

![Python Version](https://img.shields.io/badge/Python-3.13+-blue)
![License](https://img.shields.io/badge/License-MIT-green)


An AI agent powered by Google Gemini that can search the web in real-time to answer questions — built with function calling and an autonomous agent loop.

How It Works
------------------------------------------------------------------------------------------------------------------------------------------------------------
Unlike a normal chatbot that answers from training data, this agent can decide to search the web, run the search, read the results, and keep searching until it has enough information to give a confident answer.

You ask a question

      ↓
Gemini decides it needs real-time data

       ↓
Agent calls DuckDuckGo with a search query

       ↓
Results sent back to Gemini

       ↓
Gemini decides if it needs more searches

       ↓
When satisfied → Final answer


-------------------------------------------------------------------------------------------------------------------------


Layer	Tool
Language Model	Google Gemini Flash
Web Search	DuckDuckGo (free, no API key)
Function Calling	Gemini types.Tool + types.Part.from_function_response
Key Concepts

Function Calling — Gemini doesn't run tools itself. It tells your code "I want to call this tool with these arguments." Your Python code runs the tool and sends the results back.

Agent Loop — The agent keeps running until Gemini stops asking for tools and returns a text answer. It may search multiple times before it's confident enough to respond.

Quickstart

1. Clone the repo

  bash
  git clone https://github.com/rushiltandon05-lgtm/ai-agent
  cd ai-agent

2. Install dependencies

  bash
  pip install google-genai ddgs python-dotenv

3. Add your API key

  Create a system.env file:
  
  GEMINI_API_KEY=your_gemini_key_here
  
  Get your key from aistudio.google.com

4. Run

  bash
  python agent.py
  Example Output
  Searched: current weather Melbourne Australia
  Searched: current weather Bangalore India
  Searched: temperature in Melbourne Australia right now
  Searched: temperature in Bangalore India right now

*Final Answer:*
Currently in Melbourne, Australia it is partly cloudy with a temperature of
14°C. In Bangalore, India it is warm at 26°C with light rain showers.
Project Structure
ai-agent/
├── agent.py       # Main agent — function calling + agent loop
├── system.env     # API keys (not committed to Git)
└── .gitignore
Built With
Google Gemini API — language model + function calling
DuckDuckGo Search (ddgs) — free web search, no API key needed
