"""Tool registry dispatcher and execution handler for agent tool calls."""

import json
from collections.abc import Callable

from openai.types.chat import (
    ChatCompletionMessageToolCallUnion,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
)
from openai.types.chat.chat_completion_message_custom_tool_call import (
    ChatCompletionMessageCustomToolCall,
)

from aiagent.functions.get_file_content import get_file_content, schema_get_file_content
from aiagent.functions.get_files_info import get_files_info, schema_get_files_info
from aiagent.functions.run_python_file import run_python_file, schema_run_python_file
from aiagent.functions.write_file import schema_write_file, write_file

available_functions: list[ChatCompletionToolParam] = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(
    tool_call: ChatCompletionMessageToolCallUnion, verbose: bool = False
) -> ChatCompletionToolMessageParam:
    """Dispatch and execute an LLM tool call against registered functions.

    Parameters
    ----------
    tool_call : ChatCompletionMessageToolCallUnion
        The tool call payload received from the chat completion response.
    verbose : bool, default=False
        Whether to print diagnostic tool invocation details.

    Returns
    -------
    ChatCompletionToolMessageParam
        Tool response message dict containing the execution output.
    """
    if isinstance(tool_call, ChatCompletionMessageCustomToolCall):
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unsupported tool call type: {tool_call.type}",
        }

    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }

    working_directory = "./calculator"
    function_args["working_directory"] = working_directory

    result = function_map[function_name](**function_args)

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
