# Findings Log — How to Use This

This CSV is your working evidence trail throughout the two-week engagement.
Import it into Excel or Google Sheets and keep it updated daily — it is
where your Security Assessment Report's claims should trace back to.

## Columns

- **date_logged** — the date you actually confirmed this finding, not the
  date you started the project. Fill this in as you go.
- **finding_id** — keep the F1–F5 numbering for the five primary incidents
  from the case study; add F6, F7, etc. for anything additional you
  discover during the engagement (and you likely will — see the note in
  `app/main.py` about the unauthenticated customer_id parameter).
- **category** — Identity / Data / Network / AI Workload / Governance
- **severity** — Critical / High / Medium / Low. Be ready to justify this
  in the Live Defense Session.
- **status** — Open → In Progress → Remediated, or → Residual Risk if it's
  staying open by the end of the engagement (with a documented reason).
- **evidence_location** — where the actual proof lives: a screenshot
  filename, a terminal output you've saved, a Secure Score capture date.
  Be specific enough that you (or your mentor) could find it again.
- **notes** — anything else worth remembering when you write the final
  report — context that won't fit cleanly into the other columns.

## Why this matters

Every finding in your final Security Assessment Report should be
traceable back to a row in this log. In the Live Defense Session, your
mentor may ask you to pull up the evidence behind a specific claim — if
you've kept this log updated honestly throughout, that's a five-second
lookup. If you've been improvising the report from memory at the end of
Week 2, it won't be.
