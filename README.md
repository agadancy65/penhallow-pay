# Penhallow Pay — Spending Insights

**Cloud Security Posture Assessment & AI Workload Protection**
Amdari Cloud Security Internship Programme — Senior Cohort

---

## What this repository is

This is the starter codebase for the Penhallow Pay engagement described in
your Case Study document. It contains:

- A working FastAPI application (`/app`) — the "Spending Insights" AI
  chatbot — deliberately wired with the vulnerability described as
  **Incident 1** in the case study (a hardcoded Cognitive Services API key).
- Bicep infrastructure templates (`/infrastructure`) that provision the
  full vulnerable starting environment in your own Azure subscription,
  matching **Incidents 2 and 3** (public Storage Account, unrestricted
  Cognitive Services endpoint).
- Starter policy definitions (`/infrastructure/policies`) for the
  guardrails you'll author in Week 2.
- Report templates (`/docs`) for the Security Assessment Report and
  Findings Log that are the actual deliverables of this engagement.

⚠️ **Do not fix anything before you've read the Case Study document in
full and reached the relevant day in the Weekly Schedule.** Several files
in this repository are intentionally vulnerable — see the warning
comments at the top of `app/config.py` and `infrastructure/main.bicep`.
The diagnostic value of this engagement depends on confirming each
incident with real evidence before remediating it.

---

## Quick Start

### 1. Clone and set up the Python environment

```bash
git clone <this-repo-url> penhallow-pay
cd penhallow-pay

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Register required Azure resource providers

Free-tier subscriptions often have these unregistered, which causes the
single most common Day 1 blocker. Run this before deploying anything:

```bash
az login

az provider register --namespace Microsoft.CognitiveServices
az provider register --namespace Microsoft.PolicyInsights
az provider register --namespace Microsoft.KeyVault
az provider register --namespace Microsoft.Security
az provider register --namespace Microsoft.Storage

# Check status (repeat until "Registered"):
az provider show --namespace Microsoft.CognitiveServices --query registrationState
```

### 3. Deploy the vulnerable starting environment

```bash
cd infrastructure

az group create --name rg-penhallow-poc --location uksouth

# Edit parameters.json first — set uniqueSuffix to your initials
az deployment group create \
  --resource-group rg-penhallow-poc \
  --template-file main.bicep \
  --parameters @parameters.json
```

This provisions exactly the environment described in the case study's
incident history: a publicly readable Storage Account, an unrestricted
Cognitive Services resource, and an App Service with the API key baked
into its configuration.

### 4. Upload the sample transaction export (to make Incident 2 tangible)

```bash
az storage blob upload \
  --account-name <storage-account-name-from-deployment-output> \
  --container-name transaction-exports \
  --name may-2026-export.csv \
  --file infrastructure/sample-transaction-export.csv \
  --auth-mode login
```

After this, the file should be readable at the public blob URL with no
authentication — confirm this yourself in an incognito browser window as
part of Week 1, Tuesday.

### 5. Run the application locally

```bash
cp .env.example .env
# Edit .env with your deployed Cognitive Services endpoint and key

cd app
uvicorn main:app --reload --port 8000
```

Visit `http://localhost:8000` to see the Spending Insights chat interface.

---

## Repository Structure

```
penhallow-pay/
├── app/
│   ├── main.py              # FastAPI application + routes
│   ├── config.py            # ⚠️ Contains the planted hardcoded API key
│   ├── transactions.py      # Mock customer transaction data
│   ├── chatbot.py           # Cognitive Services integration + AI risk notes
│   ├── templates/index.html # Chat UI
│   └── static/               # CSS + JS for the frontend
├── infrastructure/
│   ├── main.bicep           # ⚠️ Provisions the vulnerable starting environment
│   ├── parameters.json
│   ├── sample-transaction-export.csv
│   └── policies/
│       ├── deny-public-storage.json    # Worked example
│       ├── README.md                    # What you need to author
│       └── (you add: audit-static-key-auth.json)
├── docs/
│   ├── report-template/
│   │   └── Security_Assessment_Report_Template.md
│   ├── findings-log/
│   │   ├── findings-log-template.csv
│   │   └── README.md
│   └── ai-risk-analysis-template.md
├── .github/workflows/
│   └── security-scan.yml    # Reference TruffleHog + pip-audit workflow
├── requirements.txt
├── .env.example
└── README.md                 # You are here
```

---

## Where Each Deliverable Lives

| Deliverable | Location |
|---|---|
| Findings Log (your working evidence trail) | `/docs/findings-log/` |
| Security Assessment Report (final submission) | Built from `/docs/report-template/` |
| AI Risk Analysis (Week 2, Tuesday) | Built from `/docs/ai-risk-analysis-template.md` |
| Guardrail policies (Week 2, Wednesday) | `/infrastructure/policies/` |

---

## A Note on Cost

Every resource in this template is provisioned on Azure's free tier or
free-tier-equivalent SKU (Storage `Standard_LRS`, Cognitive Services `F0`,
App Service `F1`). Running this project end-to-end should cost effectively
nothing on a standard Azure free-tier subscription, provided you delete
the resource group when the engagement concludes:

```bash
az group delete --name rg-penhallow-poc --yes --no-wait
```

---

*This is a fictional company and a fictional engagement, built for the
Amdari Cloud Security Internship Programme. No real customer data is used
anywhere in this repository.*
