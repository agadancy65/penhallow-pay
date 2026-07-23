"""
Spending Insights chatbot logic — calls Azure Cognitive Services (Azure
OpenAI-compatible endpoint) to answer natural-language questions about a
customer's transaction history.

==============================================================================
 AI-SPECIFIC SECURITY NOTE (relevant to Week 2, Tuesday)
==============================================================================
This module is the part of the codebase most relevant to your AI risk
analysis. A few things worth noticing as you read it:

1. The full transaction history is serialised directly into the prompt
   sent to the model (see _build_prompt below). This means the model has
   access to everything in that customer's transaction list for every
   single question — including questions that have nothing to do with
   the data being exposed. A user asking an unrelated or cleverly-phrased
   question could potentially get the model to reveal more than intended.

2. There is no validation on the `question` field before it reaches the
   model. A production system would typically apply Content Safety
   filtering (Week 2, Tuesday) before sending user input to the model,
   and again on the model's output before returning it to the user.

3. The system prompt below is a soft instruction, not a hard boundary —
   language models can be persuaded to deviate from system instructions
   through carefully crafted user input ("prompt injection"). This is
   precisely why Content Safety filtering and tight scoping of what data
   reaches the model are defence-in-depth measures, not optional extras.

You are not required to fix all of this during the engagement — the case
study scopes the AI security work to authentication, network restriction,
and Content Safety. But your written risk analysis should demonstrate you
understand these dynamics, even where full remediation is out of scope.
==============================================================================
"""

import logging
from openai import AzureOpenAI

logger = logging.getLogger("penhallow.chatbot")

_SYSTEM_PROMPT = """You are Penhallow Pay's Spending Insights assistant.
You help customers understand their own transaction history. Answer
questions clearly and concisely, referencing specific transactions or
totals where helpful. Only discuss the transaction data provided to you
in this conversation. Do not make up transactions that are not in the
provided data."""


def _build_prompt(question: str, transactions: list[dict]) -> str:
    """
    Serialise the customer's transaction list into the prompt context.

    See the module docstring above — this is the part of the system
    most relevant to the AI-specific risk analysis expected in Week 2.
    """
    transaction_lines = "\n".join(
        f"- {t['date']}: {t['merchant']} ({t['category']}) — £{t['amount']:.2f}"
        for t in transactions
    )
    return (
        f"Here is the customer's transaction history:\n\n{transaction_lines}\n\n"
        f"Customer question: {question}"
    )


def answer_spending_question(
    question: str, transactions: list[dict], credentials: dict
) -> str:
    """
    Call Azure Cognitive Services to answer a spending-related question.

    `credentials` is the dict returned by config.get_cognitive_services_credentials()
    — contains `endpoint` and `key`.
    """
    client = AzureOpenAI(
        azure_endpoint=credentials["endpoint"],
        api_key=credentials["key"],
        api_version="2024-02-01",
    )

    user_prompt = _build_prompt(question, transactions)

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",  # deployment name on the Cognitive Services resource
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_completion_tokens=1000,
        )
        return response.choices[0].message.content

    except Exception as exc:
        logger.error(f"Azure Cognitive Services call failed: {exc}")
        raise
