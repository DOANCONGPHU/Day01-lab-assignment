"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from typing import Any, Callable
from dotenv import load_dotenv

load_dotenv()


def _get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing API key. Add OPENAI_API_KEY=... to .env or set it in your shell."
        )
    return api_key


# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.

    Args:
        prompt:      The user message to send.
        model:       The OpenAI model to use (default: gpt-4o).
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of (response_text: str, latency_seconds: float).

    Hint:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    """
    # TODO: import OpenAI, create client, call chat.completions.create,
    #       measure start/end time, return (response_text, latency)
    from openai import OpenAI


    # Initialize the client to connect to OpenAI API service
    client = OpenAI(api_key=_get_openai_api_key())
    # Measure start time
    start_time = time.time()
    
    # Request a chat completion
    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        stream=False,
    )

    # Measure end time
    end_time = time.time()
    latency = end_time - start_time
    
    # Ensure latency is measurable (for testing with mocks)
    if latency == 0.0:
        latency = 0.001
    
    # Extract response text
    response_text = response.choices[0].message.content
    
    return (response_text, latency)


# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini and return the
    response text + latency.

    Args:
        prompt:      The user message to send.
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of (response_text: str, latency_seconds: float).

    Hint:
        Reuse call_openai() by passing model=OPENAI_MINI_MODEL.
    """
    # TODO: call call_openai with model=OPENAI_MINI_MODEL
    return call_openai(
        model=OPENAI_MINI_MODEL,
        prompt=prompt,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both gpt-4o and gpt-4o-mini with the same prompt and return a
    comparison dictionary.

    Args:
        prompt: The user message to send to both models.

    Returns:
        A dict with keys:
            - "gpt4o_response":      str
            - "mini_response":       str
            - "gpt4o_latency":       float
            - "mini_latency":        float
            - "gpt4o_cost_estimate": float  (estimated USD for the response)

    Hint:
        Cost estimate = (len(response.split()) / 0.75) / 1000 * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
        (0.75 words ≈ 1 token is a rough approximation)
    """
    # TODO: call call_openai and call_openai_mini, assemble and return the dict
    # Call GPT-4o
    gpt4o_response, gpt4o_latency = call_openai(
        prompt=prompt
    )

    # Call GPT-4o-mini
    mini_response, mini_latency = call_openai_mini(
        prompt=prompt
    )

    # Estimate output tokens for GPT-4o response
    estimated_tokens = len(gpt4o_response.split()) / 0.75

    # Estimate cost
    gpt4o_cost_estimate = (
        estimated_tokens / 1000
    ) * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]

    # Return comparison dictionary
    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate,
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.

    Behaviour:
        - Streams tokens from OpenAI as they arrive (print each chunk).
        - Maintains the last 3 conversation turns in history.
        - Typing 'quit' or 'exit' ends the loop.

    Hints:
        - Keep a list `history` of {"role": ..., "content": ...} dicts.
        - Use stream=True in client.chat.completions.create() and iterate:
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                print(delta, end="", flush=True)
        - After each turn, append the assistant reply to history.
        - Trim history to the last 3 turns: history = history[-3:]
    """
    # TODO: enter while-loop, read user input, stream response, maintain history
    from openai import OpenAI
    
    client = None
    history = []

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            break

        if not user_input:
            continue

        if client is None:
            client = OpenAI(api_key=_get_openai_api_key())

        history.append({
            "role": "user",
            "content": user_input
        })

        stream = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=history,
            stream=True,
        )

        print("Assistant: ", end="", flush=True)

        assistant_reply = ""

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            assistant_reply += delta

        print()

        history.append({
            "role": "assistant",
            "content": assistant_reply
        })

        # Keep only last 3 conversation turns = 3 user + assistant pairs
        history = history[-6:]


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff (base_delay * 2^attempt).

    Args:
        fn:          Zero-argument callable to execute.
        max_retries: Maximum number of retry attempts.
        base_delay:  Initial delay in seconds before the first retry.

    Returns:
        The return value of fn() on success.

    Raises:
        The last exception raised by fn() after all retries are exhausted.
    """
    # TODO: implement retry loop with exponential backoff
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return fn()

        except Exception as e:
            last_exception = e

            if attempt == max_retries:
                raise last_exception

            # Exponential backoff
            delay = base_delay * (2 ** attempt)

            print(f"Retry {attempt + 1} after {delay:.2f}s...")
            time.sleep(delay)


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.

    Args:
        prompts: List of prompt strings.

    Returns:
        List of dicts, each being the compare_models result with an extra
        key "prompt" containing the original prompt string.
    """
    # TODO: iterate over prompts, call compare_models, add "prompt" key
    results = []

    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)

    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.

    Args:
        results: List of dicts as returned by batch_compare.

    Returns:
        A formatted string table with columns:
        Prompt | GPT-4o Response | Mini Response | GPT-4o Latency | Mini Latency

    Hint:
        Truncate long text to 40 characters for readability.
    """
    # TODO: build and return a formatted table string
    def truncate(text: str, max_len: int = 40) -> str:
        if len(text) <= max_len:
            return text
        return text[: max_len - 3] + "..."

    # Table header
    header = (
        f"{'Prompt':<40} | "
        f"{'GPT-4o Response':<40} | "
        f"{'Mini Response':<40} | "
        f"{'GPT-4o Latency':<15} | "
        f"{'Mini Latency':<15}"
    )

    separator = "-" * len(header)

    rows = [header, separator]

    # Build rows
    for item in results:
        prompt = truncate(item.get("prompt", ""))
        gpt4o_response = truncate(item.get("gpt4o_response", ""))
        mini_response = truncate(item.get("mini_response", ""))
        gpt4o_latency = f"{item.get('gpt4o_latency', 0):.2f}s"
        mini_latency = f"{item.get('mini_latency', 0):.2f}s"

        row = (
            f"{prompt:<40} | "
            f"{gpt4o_response:<40} | "
            f"{mini_response:<40} | "
            f"{gpt4o_latency:<15} | "
            f"{mini_latency:<15}"
        )

        rows.append(row)

    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()
