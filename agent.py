from google import genai
from google.genai import types
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv("system.env")

use_web_declaration = {
    "name": "use_web_declaration",
    "description": "Uses DuckDuckGo's search engine to confirm answers whose current data is not known or needed based on recent data or need references to",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to look up on the web"
            }
        },
        "required": ["query"]
    }
}

def use_web(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            return results if results else "No results found"
    except Exception as e:
        return f"Search failed: {str(e)}"

client = genai.Client()
tools = types.Tool(function_declarations=[use_web_declaration])
config = types.GenerateContentConfig(tools=[tools])

user_question = "What is the current weather of Melbourne Australia and Bangalore India?"

current_response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=user_question,
    config=config
)

conversation = [
    types.Content(role="user", parts=[types.Part(text=user_question)]),
]

while True:
    function_response_parts = []
    has_function_call = False

    for part in current_response.candidates[0].content.parts:
        if part.function_call:
            has_function_call = True
            tools_name = part.function_call.name
            tools_arg = part.function_call.args
            if tools_name == "use_web_declaration":
                result = use_web(tools_arg["query"])
                print(f"Searched: {tools_arg['query']}")
                function_response_parts.append(
                    types.Part.from_function_response(
                        name=tools_name,
                        response={"result": result},
                    )
                )

    if not has_function_call:
        for part in current_response.candidates[0].content.parts:
            if hasattr(part, 'text') and part.text:
                print("\nFinal Answer:")
                print(part.text)
        break

    conversation.append(current_response.candidates[0].content)
    conversation.append(types.Content(role="user", parts=function_response_parts))

    current_response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=conversation,
        config=config
    )