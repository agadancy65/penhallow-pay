/*
  Penhallow Pay — Vulnerable Starting Environment
  =================================================

  ⚠️  THIS TEMPLATE DELIBERATELY PROVISIONS AN INSECURE ENVIRONMENT.

  Every resource here is intentionally misconfigured to match the five
  incidents described in the Penhallow Pay case study:

    Incident 1 — App Service deployed with a hardcoded Cognitive Services
                 key in its application settings (see appSettings below).
    Incident 2 — Storage Account with public blob access enabled.
    Incident 3 — Cognitive Services resource with no network restriction,
                 reachable from any network.
    Incident 4 — No Defender for Cloud plans enabled beyond the free
                 Foundational CSPM tier (this is the default state — no
                 action needed to "create" this incident, only to fix it).
    Incident 5 — No Azure Policy assignments preventing recurrence.

  DO NOT "fix" anything in this file before deploying. The whole point of
  this template is to give every intern an identical, reproducible broken
  environment to diagnose and remediate themselves, by hand, in the Azure
  Portal and CLI — not by editing this template.

  Deploy with:
    az deployment group create \
      --resource-group rg-penhallow-poc \
      --template-file main.bicep \
      --parameters @parameters.json
*/

@description('A short, unique suffix to avoid global naming collisions (e.g. your initials + a number)')
param uniqueSuffix string

@description('Azure region for all resources')
param location string = 'uksouth'

@description('Environment tag applied to all resources')
param environment string = 'poc'

// ──────────────────────────────────────────────────────────────────────────
// Storage Account — Incident 2: public blob access enabled
// ──────────────────────────────────────────────────────────────────────────
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'stpenhallow${uniqueSuffix}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    // ⚠️ VULNERABLE: public access enabled — this is Incident 2
    allowBlobPublicAccess: true
    minimumTlsVersion: 'TLS1_0'
    supportsHttpsTrafficOnly: false
    accessTier: 'Hot'
  }
  tags: {
    environment: environment
    project: 'penhallow-pay'
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
}

resource transactionExportsContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: 'transaction-exports'
  properties: {
    // ⚠️ VULNERABLE: container-level public access — required in addition
    // to the account-level flag above for the container to actually be
    // publicly readable (see solution guide troubleshooting notes)
    publicAccess: 'Container'
  }
}

// ──────────────────────────────────────────────────────────────────────────
// Cognitive Services — Incident 3: no network restriction, key-based auth
// ──────────────────────────────────────────────────────────────────────────
resource cognitiveServices 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: 'cog-penhallow-${uniqueSuffix}'
  location: location
  sku: {
    name: 'F0' // Free tier — keeps this project within Azure free-tier limits
  }
  kind: 'CognitiveServices'
  properties: {
    // ⚠️ VULNERABLE: no custom domain set, no network ACLs restricting
    // access — the resource accepts requests from any network using
    // just the API key, which is itself hardcoded in the app (Incident 1)
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
  tags: {
    environment: environment
    project: 'penhallow-pay'
  }
}

// ──────────────────────────────────────────────────────────────────────────
// App Service Plan + App Service — hosts the Spending Insights chatbot
// ──────────────────────────────────────────────────────────────────────────
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: 'asp-penhallow-${uniqueSuffix}'
  location: location
  sku: {
    name: 'F1' // Free tier
    tier: 'Free'
  }
  properties: {
    reserved: true // Linux
  }
}

resource appService 'Microsoft.Web/sites@2023-01-01' = {
  name: 'penhallow-spending-insights-${uniqueSuffix}'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      appSettings: [
        {
          name: 'COGNITIVE_SERVICES_ENDPOINT'
          value: cognitiveServices.properties.endpoint
        }
        {
          // ⚠️ VULNERABLE: this is Incident 1 — the API key is written
          // directly into App Service application settings, mirroring
          // how it sits hardcoded in app/config.py in the repository.
          // In a real engagement this would also be flagged separately
          // as "secret visible in deployment configuration" in addition
          // to "secret hardcoded in source control" — two related but
          // distinct findings worth naming separately in your report.
          name: 'COGNITIVE_SERVICES_KEY'
          value: cognitiveServices.listKeys().key1
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
      ]
    }
  }
  tags: {
    environment: environment
    project: 'penhallow-pay'
  }
}

// ──────────────────────────────────────────────────────────────────────────
// Outputs — used by deployment scripts and verification steps
// ──────────────────────────────────────────────────────────────────────────
output storageAccountName string = storageAccount.name
output cognitiveServicesName string = cognitiveServices.name
output cognitiveServicesEndpoint string = cognitiveServices.properties.endpoint
output appServiceName string = appService.name
output appServiceDefaultHostname string = appService.properties.defaultHostName
output transactionExportsPublicUrl string = '${storageAccount.properties.primaryEndpoints.blob}transaction-exports/'
