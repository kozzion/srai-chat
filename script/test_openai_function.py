import os

from openai import OpenAI


def chat_completion_request(messages, tools=None, tool_choice=None, model="gpt-3.5-turbo"):
    client_openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    print(model)
    print(messages)
    print(tools)
    print(tool_choice)
    completion = client_openai.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice=tool_choice,
    )
    return completion


tools = [
    {
        "type": "function",
        "function": {
            "name": "image_tag",
            "description": "Get the docker image tag of the image the bot is currently running",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    }
]


messages = []
messages.append(
    {
        "role": "system",
        "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.",
    }
)
messages.append({"role": "user", "content": "What image tag is the bot running"})
chat_response = chat_completion_request(messages, tools=tools)
assistant_message = chat_response.choices[0].message
messages.append(assistant_message)
print(messages)
