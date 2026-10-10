import os
from typing import cast

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from functions.call_functions import available_functions, call_function
from prompts import system_prompt


class AgentService:
    def __init__(self) -> None:
        api_key = os.environ.get("OPENROUTER_API_KEY", "dummy_key_if_not_provided_for_tests")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def run_agent(self, user_prompt: str, verbose: bool = False) -> str:
        """Run the AI agent conversation and tool-calling evaluation loop."""
        
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # Return a list of text responses or capture print output? 
        # For an API, it's better to capture and return the final string instead of using `print`.
        
        output_log = []

        for _ in range(20):
            response = self.client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                tools=available_functions,
            )

            if verbose:
                output_log.append(f"User prompt: {user_prompt}")
                if response.usage:
                    output_log.append(f"Prompt tokens: {response.usage.prompt_tokens}")
                    output_log.append(f"Response tokens: {response.usage.completion_tokens}")

            message = response.choices[0].message
            messages.append(cast(ChatCompletionMessageParam, message))

            if message.tool_calls:
                for tool_call in message.tool_calls:
                    result_message = call_function(tool_call, verbose)
                    messages.append(result_message)
            else:
                output_log.append(message.content or "")
                break
        else:
            output_log.append("Reached maximum number of iterations without a final response.")

        return "\n".join(output_log)
