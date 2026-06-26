# Azure Policy Definitions — Penhallow Pay Engagement

This folder is where you author the guardrail policies referenced in
Section 6.5 of the case study and Week 2, Wednesday of the schedule.

## What's already here

**`deny-public-storage.json`** is provided as a worked example so you can
see the expected shape, naming convention, and the level of detail expected
in the `description` field — notice it explains *why* the policy exists,
referencing the specific incident, not just *what* it does. Every policy
you author for your report should follow this same pattern: a description
someone unfamiliar with this engagement could read and understand the
reasoning, six months from now.

## What you need to add

**`audit-static-key-auth.json`** — your second policy from the case
study, addressing resources authenticating via static key instead of
Managed Identity where Managed Identity is available. The solution guide
discusses two valid approaches:

1. Author a fully custom policy (harder — static key usage isn't
   expressed generically across all resource types in a simple policy
   rule).
2. Assign Azure's built-in policy `"Cognitive Services accounts should
   disable local authentication"` in Audit mode, and explain in your
   report why you chose the built-in policy and why Audit (not Deny) is
   the appropriate effect here.

Either approach is acceptable. What your mentor will be evaluating in
the Live Defense Session is whether you can explain the *reasoning*
behind the effect you chose (Deny vs. Audit), not just that a policy
exists.

## Testing your policies

Don't just assign a policy and assume it works — prove it, the same way
you proved every other finding in this engagement:

```bash
# Assign at subscription scope
az policy definition create \
  --name deny-public-storage \
  --rules deny-public-storage.json \
  --mode Indexed

az policy assignment create \
  --name deny-public-storage-assignment \
  --policy deny-public-storage \
  --scope /subscriptions/<your-subscription-id>

# Prove it blocks a violation — this should fail with
# RequestDisallowedByPolicy:
az storage account create \
  --name sttestviolation$RANDOM \
  --resource-group rg-penhallow-poc \
  --allow-blob-public-access true
```

The failed command's output — specifically the `RequestDisallowedByPolicy`
error — is the evidence that belongs in your Remediation Evidence section.
