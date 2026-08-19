import json

# The JSON-schema tool list we hand to the model on every call. Diverse tasks
# need diverse tools; the agent decides which (if any) to use.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate an arithmetic expression and return the number.",
            "parameters": {
                "type": "object",
                "properties": {"expr": {"type": "string"}},
                "required": ["expr"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup",
            "description": "Look up a fact by key from a small knowledge base.",
            "parameters": {
                "type": "object",
                "properties": {"key": {"type": "string"}},
                "required": ["key"],
            },
        },
    },
]

_FACTS = {"capital_of_france": "Paris", "speed_of_light_km_s": "299792"}


def call_tool(name: str, arguments: str) -> str:
    """Dispatch a model-requested tool call to its implementation."""
    args = json.loads(arguments)
    if name == "calculator":
        return str(eval(args["expr"], {"__builtins__": {}}, {}))  # sandboxed eval
    if name == "lookup":
        return _FACTS.get(args["key"], "unknown")
    return f"error: no such tool {name}"
