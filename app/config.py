"""
Configuration for the Spending Insights chatbot's Azure Cognitive Services
connection.

==============================================================================
 ⚠️  THIS FILE CONTAINS THE PLANTED VULNERABILITY — "INCIDENT 1"
==============================================================================
As shipped, this file authenticates to Azure Cognitive Services using a
static API key, hardcoded below. This is exactly the finding described in
the Penhallow Pay case study: "a static API key... committed in plaintext
to the application's configuration file since the feature's first commit
three months ago."

DO NOT remove the hardcoded value below until Wednesday/Thursday of Week 1,
after the finding has been confirmed and logged (Tuesday). Removing it
early defeats the point of the diagnostic exercise.

------------------------------------------------------------------------------
WHAT THE FIX LOOKS LIKE (Week 1, Wednesday–Thursday)
------------------------------------------------------------------------------
Replace the contents of get_cognitive_services_credentials() below with a
Managed Identity-based lookup against Azure Key Vault. The target
implementation looks like this:

    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient

    def get_cognitive_services_credentials() -> dict:
        credential = DefaultAzureCredential()
        vault_url = os.environ["KEY_VAULT_URL"]  # e.g. https://kv-penhallow-xx.vault.azure.net
        client = SecretClient(vault_url=vault_url, credential=credential)

        return {
            "endpoint": os.environ["COGNITIVE_SERVICES_ENDPOINT"],
            "key": client.get_secret("cognitive-services-key").value,
        }

Note that even in the fixed version, the *endpoint* (a non-secret URL) can
stay as a plain environment variable — only the *key* needs to move to
Key Vault. This distinction (what's actually secret vs. what's just
configuration) is worth being explicit about in your report.
==============================================================================
"""

import os


# ──────────────────────────────────────────────────────────────────────────
# VULNERABLE VERSION (as shipped — Incident 1)
# ──────────────────────────────────────────────────────────────────────────
# This constant is the finding. A real engagement would find this same
# pattern via a secrets-scanning tool (TruffleHog, Gitleaks) or manual
# review of a private repository that nonetheless should never contain
# plaintext credentials, rotated or not.
_HARDCODED_COGNITIVE_SERVICES_KEY = "REPLACE_WITH_YOUR_OWN_TEST_KEY_DO_NOT_USE_REAL_PROD_KEYS"
_HARDCODED_ENDPOINT = "https://penhallow-spending-insights.cognitiveservices.azure.com/"


def get_cognitive_services_credentials() -> dict:
    """
    Returns the endpoint and key needed to call Azure Cognitive Services.

    VULNERABLE STATE: reads the key from the hardcoded constant above.
    Once you've completed the Key Vault migration (Week 1, Wed/Thu), this
    function should be rewritten to use DefaultAzureCredential and pull
    the secret from Key Vault at runtime — see the module docstring above
    for the target implementation.
    """
    return {
        "endpoint": os.environ.get("COGNITIVE_SERVICES_ENDPOINT", _HARDCODED_ENDPOINT),
        "key": os.environ.get("COGNITIVE_SERVICES_KEY", _HARDCODED_COGNITIVE_SERVICES_KEY),
    }
