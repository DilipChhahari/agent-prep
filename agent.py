import ollama
from tools import search_products, add_to_cart

available = {"search_products": search_products, "add_to_cart": add_to_cart}

messages = [
    {
        "role": "system",
        "content": (
            "You are a shopping assistant. Call only one tool at a time. "
            "Call search_products first and wait for its result. Then call "
            "add_to_cart using a real numeric id from that result. Never "
            "invent ids. Never say an item was added unless add_to_cart "
            "succeeded"
        ),
    },
    {
        "role": "user",
        "content": "Find books under Rs. 1500 and add the cheapest one to my cart.",
    },
]

for step in range(5):
    response = ollama.chat(
        model="qwen2.5:7b",
        messages=messages,
        tools=[search_products, add_to_cart],
    )
    messages.append(response.message)

    if not response.message.tool_calls:
        print("Answer:", response.message.content)
        break


    for call in response.message.tool_calls:
        name = call.function.name
        args = call.function.arguments
        print("Tool call:", name, args)
        result = available[name](**args)
        messages.append({"role": "tool", "tool_name": name, "content": str(result)})

from tools import cart
print("Actual cart contents:", cart)
