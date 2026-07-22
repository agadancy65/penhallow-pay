"""
Configuration for the Spending Insights chatbot's Azure Cognitive Services
connection.

==============================================================================
 SECURE VERSION — Incident 1 remediated (Week 1, Wed/Thu)
==============================================================================
This file authenticates to Azure Cognitive Services using a Managed
Identity, retrieving the API key from Azure Key Vault at runtime instead
of storing it in source code or plaintext App Settings.
==============================================================================
"""
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def get_cognitive_services_credentials() -> dict:
    credential = DefaultAzureCredential()
    vault_url = os.environ["KEY_VAULT_URL"]
    client = SecretClient(vault_url=vault_url, credential=credential)

    return {
        "endpoint": os.environ["COGNITIVE_SERVICES_ENDPOINT"],
        "key": client.get_secret("cognitive-services-key").value,
    }
