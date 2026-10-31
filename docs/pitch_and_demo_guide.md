# 🏆 TaskGuard — Hackathon Pitch & Demo Script (4 Minutes)

> **Event**: CT BuildFest 2.0 · 30-Hour Coding Hackathon  
> **Problem Statement ID**: CTBF-AI-11  
> **Target Audience**: Judges, Placement Cells, Cyber Defense Evaluators  

---

## ⏱️ 4-Minute Presentation Script

### 0:00 - 0:30 · The Hook & The Problem (30s)
> *"Judges, imagine a college student or homemaker receiving a message: 'Earn ₹5,000 a day just by liking YouTube videos.' They complete a 2-minute trial task and instantly receive a real ₹150 in their bank account. Trust is established. Then, they are invited to a 'prepaid VIP order' — deposit ₹1,000 for ₹1,300 return. Over 7 months, a victim in Kharghar lost ₹9.66 lakh across 34 transactions before realizing it was a fraud.*
>
> *Existing tools like Truecaller or SMS filters check single messages. But task fraud isn't a single message — it is an escalating 5-stage script. Today, we present **TaskGuard: the scam-stage radar that warns you before the next payment**."*

---

### 0:30 - 1:15 · Live Demo 1: The Stage 1 Hook (45s)
> *(Action: Click **Demo 1: Stage 1 Hook** preset)*
>
> *"Look at our live system. We input a conversation where a 'receptionist' on Telegram transfers a real ₹150 trial payout. A generic detector might call this genuine because money was actually received!*
>
> *TaskGuard analyzes the whole conversation: it flags **Stage 1: Hook**, shows our circular risk gauge, and crucially — our **Prediction Radar** warns: 'They will likely prompt you to join a prepaid VIP task asking for ₹1,000 to ₹5,000 with a promise of 30-50% profit.' We alert the user to the trap BEFORE it happens."*

---

### 1:15 - 2:00 · Live Demo 2: The Stage 2 Prepaid Trap (45s)
> *(Action: Click **Demo 2: Stage 2 Prepaid Trap** preset)*
>
> *"Now the conversation progresses. The scammer asks for ₹1,000 deposit to a personal UPI ID `rajeshkumar8472@ybl` promising ₹1,300 return. Watch TaskGuard in real-time:*
>
> *1. **Verdict**: SCAM DETECTED with a 90/100 Risk Score.*  
> *2. **Stage Timeline**: Highlights Stage 2 (Prepaid Trap).*  
> *3. **Forensic Evidence**: Cites exact verbatim quotes: `Deposit ₹1,000 -> Return ₹1,300`.*  
> *4. **MCA Verification**: We check official Ministry of Corporate Affairs data offline — showing no matching corporate authorization."*

---

### 2:00 - 2:45 · Live Demo 3: Genuine Offer & Language Toggle (45s)
> *(Action: Click **Demo 5: Genuine Offer**, then toggle to **ਪੰਜਾਬੀ** or **हिन्दी**)*
>
> *"One major pitfall of fraud detectors is false alarms on legitimate employment. Watch what happens when we submit an authentic Infosys campus offer letter with CIN `L85110KA1981PLC013115`.*
>
> *TaskGuard avoids false positives: verdict is **Likely Genuine** with 0 Risk Score. Our MCA engine verifies 'Infosys Limited — Found and Active' in ROC Bangalore.*
>
> *Furthermore, for accessibility across Punjab and North India, our full UI, advice, and predictions switch instantly between **English, हिन्दी, and ਪੰਜਾਬੀ** with one tap."*

---

### 2:45 - 3:30 · Live Demo 4: 1930 Cybercrime Report Pack & Model Evaluation (45s)
> *(Action: Click **Generate Formal Complaint Pack**, then navigate to **/eval**)*
>
> *"If a victim has lost money, every minute counts to freeze the mule account. TaskGuard provides a 1-tap **Call 1930 Helpline** button and generates an evidence-backed formal complaint draft with extracted UPI IDs, phone numbers, and timeline ready for `cybercrime.gov.in`.*
>
> *Finally, look at our **/eval** page: we built an internal benchmark of **60 balanced test cases** across 4 languages. Our hybrid rules + AI engine achieves **88.3% overall accuracy** and **93.3% stage accuracy** — exceeding the hackathon target of 80%."*

---

### 3:30 - 4:00 · Ethics, Privacy & Closing (30s)
> *"TaskGuard is **stateless by default** — we never store victim chat logs, and all phone numbers, UPI IDs, and Aadhaar numbers are masked locally before AI processing.*
>
> *TaskGuard doesn't just label messages. We tell citizens which stage of the script they are in, before they send their hard-earned money. Thank you!"*

---

## 🎯 Anticipated Judge Q&A Cheat Sheet

| Question | Winning Answer |
|---|---|
| **"How is this different from Truecaller or Scamio?"** | *"Truecaller checks phone numbers or individual messages against spam lists. Scamio does general phishing chat checks. In our research, we found no tool that tracks the whole conversation across multi-stage scripts, predicts what the scammer will ask next, verifies against local MCA data, and drafts a 1930 complaint pack in Hindi and Punjabi."* |
| **"Can the LLM hallucinate company data?"** | *"No. Company registration is strictly deterministic. We query a local SQLite snapshot of official MCA master data using RapidFuzz. The LLM only extracts claims; verification is 100% code-driven."* |
| **"What about false positives on genuine job offers?"** | *"We rigorously benchmarked this in our 60-case validation suite (viewable at /eval). Legitimate offers mentioning 'no fee', campus placement drives, and verified corporate domains score 0-10% risk."* |
| **"What if the internet drops during the demo?"** | *"TaskGuard has an offline-first architecture. The rules engine, MCA SQLite database, and stage state machine operate locally without any internet connection."* |
| **"Can TaskGuard stop payments or recover money?"** | *"No software can legally block private UPI apps. Instead, TaskGuard empowers victims before the transfer, and formats immediate complaint packs for the 1930 helpline to enable bank account liens under Section 102 CrPC."* |
