# AI Workload Risk Analysis — Spending Insights Chatbot

**Author:** [Your Name]
**Date:** [Date]

This document is the written deliverable from Week 2, Tuesday of the
schedule. It should be specific to the Spending Insights feature — not a
generic list of LLM security risks copied from a blog post or the OWASP
LLM Top 10. Use the structure below, but write every section in your own
words, grounded in what this specific chatbot actually does.

---

## 1. What Makes This Endpoint Different From a Standard API

[A conventional REST API has fixed endpoints and predictable input
validation rules. Explain, specifically for `/api/chat` in this codebase,
why a generic API security checklist (auth, rate limiting, input
validation) is necessary but not sufficient here.]

---

## 2. Data Exposure via Natural-Language Queries

[Look at `app/chatbot.py` — specifically `_build_prompt()`. The customer's
full transaction history is serialised into the prompt context for every
question. Explain, in your own words, the risk this creates: could a
customer ask a question designed to extract more information than
intended? Could a cleverly-worded question cause the model to reveal
something about the system itself rather than the customer's own data?]

---

## 3. Prompt Injection Risk

[The system prompt in `chatbot.py` is a soft instruction the model
generally follows but is not architecturally guaranteed to follow.
Explain what prompt injection means in the context of this specific
chatbot, and give a concrete (hypothetical) example of a question a
malicious or curious customer might try.]

---

## 4. Why Standard Network/WAF Protection Isn't Enough

[A Web Application Firewall is tuned to catch patterns like SQL
injection and XSS. Explain why a WAF sitting in front of this chatbot
endpoint would not meaningfully reduce the risks described in Sections
2 and 3 above.]

---

## 5. What This Engagement Addressed, and What It Didn't

[Be honest and specific. This engagement's scope (per the case study)
covered: authentication (Managed Identity), network restriction (no
longer reachable from the open internet), and Content Safety filtering.
List explicitly what risk each of those three controls reduces — and
name at least one risk from Sections 2–3 above that none of them fully
solve. That gap belongs in your Security Assessment Report's Residual
Risk section.]

---

## 6. Plain-Language Summary for the Executive Summary

[Write 3–4 sentences here, suitable for a non-technical board member,
summarising the core AI-specific risk and what was done about it. This
is the version that should actually appear (or be closely adapted) in
your final report's Executive Summary.]
