import argparse
import os
import sys
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from functions.call_functions import available_functions, call_function
from prompts import system_prompt


def main(args: argparse.Namespace) -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Couldn't find OPENROUTER_API_KEY in .env")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            if response.usage:
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
            else:
                raise RuntimeError("No usage information returned from the API.")

        message = response.choices[0].message
        messages.append(cast(ChatCompletionMessageParam, message))

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
        else:
            print(message.content)
            break
    else:
        print("Reached maximum number of iterations without a final response.")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    main(args)
