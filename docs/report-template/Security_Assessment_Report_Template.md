# Penhallow Pay Ltd — Security Assessment Report

**Prepared by:** [Your Name]
**Engagement dates:** [Start date] – [End date]
**Report date:** [Date]
**Classification:** Confidential — Penhallow Pay Internal Use

---

## 1. Executive Summary

*One page maximum. Written for the CTO and the board — assume no technical
background. State the starting security posture, what was found, what was
fixed, and what remains. Lead with the number that matters most: your
Secure Score delta.*

[Write 3–4 short paragraphs here. A useful structure:
- Paragraph 1: Why this engagement happened (the penetration test, the FCA
  renewal context) and what you were asked to do.
- Paragraph 2: What you found, in plain terms — no jargon. How serious was
  it, in business terms (data exposed, duration, regulatory risk)?
- Paragraph 3: What you fixed, and what that means in practice (e.g.
  "customer transaction data is no longer accessible without authentication").
- Paragraph 4: What remains, and what you'd recommend doing next.]

**Secure Score: [starting %] → [final %]**

---

## 2. Findings

*Every finding gets its own entry. Use the table below as the format for
each one — copy it as many times as you have findings. Severity should be
justified, not just asserted.*

### Finding [N]: [Short title]

| Field | Detail |
|---|---|
| **Severity** | Critical / High / Medium / Low |
| **Category** | Identity / Data / Network / AI Workload / Governance |
| **Discovered** | [Date] |
| **Status** | Remediated / Partially Remediated / Residual Risk |

**Description**
[What was wrong, in plain language. What could go wrong as a result?]

**Evidence**
[Screenshot reference, command output, or Secure Score delta — cite the
exact entry in your Findings Log this draws from.]

**Business Impact**
[Translate the technical finding into what it means for Penhallow — data
exposure, regulatory risk, reputational risk. This is the sentence a board
member actually needs.]

---

*(Repeat the Finding block above for every finding — expect 5–8 entries
covering the five primary incidents plus anything additional you
discovered during the engagement.)*

---

## 3. Remediation Evidence

*For every finding marked "Remediated" above, provide concrete before/after
proof here. This section is what makes the report defensible — a claim
of "fixed" with no evidence is not credible.*

### [Finding N] — Remediation Evidence

**Before:**
[Screenshot/output reference]

**After:**
[Screenshot/output reference]

**Verification method:**
[How did you confirm the fix actually works — not just that you made a
change, but that the change had the intended effect?]

---

## 4. Residual Risk

*This is the most important section in the report, and the one most
people are tempted to leave thin. Be honest. A credible Residual Risk
section names real gaps and explains, with a real reason, why they sit
outside this engagement's scope.*

| Item | Why It's Not Fully Addressed | Recommended Priority |
|---|---|---|
| [e.g. Full Microsoft Purview data governance rollout] | [e.g. Two-week engagement scope covered initial classification only; full label policy and DLP rules require ongoing governance work beyond a fixed-term assessment] | High / Medium / Low |

*Add a row for every genuine gap. If you cannot think of at least one,
that is itself worth examining honestly before submission — it is
extremely unlikely that a two-week engagement leaves zero residual risk.*

---

## 5. Recommendations Beyond Scope

*What would you prioritise next if Penhallow extended this engagement?
This is where you demonstrate forward thinking beyond the fixed deliverables.*

1. [Recommendation 1 — with a one-line justification]
2. [Recommendation 2 — with a one-line justification]
3. [Recommendation 3 — with a one-line justification]

---

## Appendix A — Secure Score Detail

[Insert your starting and final Secure Score screenshots here, with
dates/timestamps visible.]

## Appendix B — Findings Log Reference

[Link or reference to your full Findings Log, maintained throughout the
engagement — every claim in this report should be traceable back to a
dated entry there.]
