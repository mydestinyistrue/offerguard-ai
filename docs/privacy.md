# 🔐 TaskGuard Privacy Policy

**Last updated**: 30 October 2026

## What TaskGuard Does

TaskGuard analyses text you submit (job offers, chat conversations, offer letters) to identify potential task scams. It provides guidance — **not legal advice**.

## Data Handling

### What We Collect
- **Nothing by default.** TaskGuard is stateless. Your submitted text is analysed in memory and discarded after the response is sent.

### PII Masking
Before any AI analysis, TaskGuard automatically masks:
- Phone numbers (replaced with `[PHONE_1]`, `[PHONE_2]`, etc.)
- UPI IDs (replaced with `[UPI_1]`, `[UPI_2]`, etc.)
- Bank account numbers (replaced with `[BANK_1]`, `[BANK_2]`, etc.)
- Aadhaar-like numbers (replaced with `[AADHAAR_1]`, `[AADHAAR_2]`, etc.)
- Email addresses (replaced with `[EMAIL_1]`, `[EMAIL_2]`, etc.)

The mapping is kept only in your browser session so you can restore details in your report pack.

### What We Do NOT Do
- ❌ Store your chats or messages
- ❌ Create user accounts or profiles
- ❌ Track your browsing or usage patterns
- ❌ Share data with third parties
- ❌ Log raw conversation text
- ❌ Store PII on our servers

### Anonymous Metrics (Optional)
If enabled, we may collect:
- Verdict distribution (e.g., "60% Scam, 30% Suspicious")
- Average analysis latency
- Language preference counts

These contain **no personal information**.

## AI Processing

- Your masked text is sent to Google Gemini API for analysis
- Google's [AI terms of service](https://ai.google.dev/terms) apply to that processing
- We use structured output only — the AI does not freely generate text about your data
- Evidence quotes are verified against your original input

## Your Rights

- You can close the browser tab at any time — no data persists
- You can use the app without an internet connection (rules-only mode)
- You control whether to share your report with authorities

## Report Pack

The report pack feature prepares information for India's cybercrime helpline (1930) and cybercrime.gov.in. This is **generated locally in your browser** and only shared when you choose to file a report.

## Contact

For privacy questions, contact the development team through the project's GitHub repository.

---

*TaskGuard is a hackathon project. It provides guidance, not legal advice. Always consult appropriate authorities for legal matters.*
