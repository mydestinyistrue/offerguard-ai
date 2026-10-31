"""Localization service for English, Hindi, and Punjabi translations."""

from __future__ import annotations

from typing import Any
from app.models.schemas import Language, Verdict


TRANSLATIONS = {
    "en": {
        "verdict_labels": {
            Verdict.SCAM: "SCAM DETECTED",
            Verdict.SUSPICIOUS: "SUSPICIOUS / HIGH RISK",
            Verdict.LIKELY_GENUINE: "LIKELY GENUINE",
            Verdict.UNSURE: "NEEDS MORE INFO / CAUTION",
        },
        "stage_names": {
            0: "Stage 0 — Bait",
            1: "Stage 1 — Hook & Small Payouts",
            2: "Stage 2 — Prepaid Trap",
            3: "Stage 3 — Lock-in & Frozen Funds",
            4: "Stage 4 — Exit Scam",
        },
        "stage_descriptions": {
            0: "The scammer makes initial unsolicited contact with an exaggerated salary offer for simple tasks.",
            1: "The scammer sends small real payouts (₹150 - ₹500) or adds you to a group to build psychological trust.",
            2: "You are asked to deposit your own money for 'VIP / merchant tasks' with a promise of quick returns.",
            3: "Your balance is locked. The scammer demands more money for 'GST, tax, unfreeze fee, or error penalty'.",
            4: "The group is deleted, your number is blocked, or a fake 'recovery agent' approaches you.",
        },
        "next_likely_moves": {
            0: "They will invite you to Telegram or WhatsApp, ask you to do a simple trial task (like a video or rating), and send you a small token payment (₹100-₹200) to gain your trust.",
            1: "They will prompt you to join a 'prepaid task' or 'VIP order', asking you to transfer ₹1,000 to ₹5,000 to a personal UPI ID with a promise of 30-50% instant profit.",
            2: "Once you transfer money, they will claim you made a mistake or need a 'combo task', asking for ₹10,000+ more before you can withdraw anything.",
            3: "They will demand more money claiming 'government tax', 'TDS', or 'security bond'. Do NOT pay — they will never release the funds and will eventually block you.",
            4: "Beware of people claiming to be 'cyber recovery specialists' or 'lawyers' who can recover your money for an upfront fee — this is a secondary scam.",
        },
        "default_advice": {
            Verdict.SCAM: [
                "DO NOT send any money, registration fees, or deposits under any circumstances.",
                "Take screenshots of all chats, UPI handles, bank accounts, and transaction IDs immediately.",
                "Immediately call the National Cyber Crime Helpline at 1930 to report the fraud and freeze the receiver account.",
                "Block and report the contact on WhatsApp/Telegram after capturing evidence.",
            ],
            Verdict.SUSPICIOUS: [
                "Never pay money to get a job. Legitimate employers never charge candidates for work or equipment.",
                "Verify the company directly on the official MCA portal (mca.gov.in) and company website.",
                "Do not move to private Telegram groups or share OTPs, bank accounts, or Aadhaar details.",
            ],
            Verdict.LIKELY_GENUINE: [
                "This offer exhibits standard recruitment patterns without upfront payment demands.",
                "Still, always verify the recruiter's official corporate email domain before submitting confidential documents.",
                "Never share net banking passwords, OTPs, or credit card details with any recruiter.",
            ],
            Verdict.UNSURE: [
                "The message contains limited information to make a definitive determination.",
                "Exercise extreme caution: if they ask for money, private chat migration, or personal banking info, treat it as a scam.",
                "Ask for an official job description and corporate email from a company domain.",
            ],
        },
    },
    "hi": {
        "verdict_labels": {
            Verdict.SCAM: "धोखाधड़ी (स्कैम) की पुष्टि",
            Verdict.SUSPICIOUS: "संदिग्ध / उच्च जोखिम",
            Verdict.LIKELY_GENUINE: "संभावित रूप से असली",
            Verdict.UNSURE: "अस्पष्ट / सावधानी बरतें",
        },
        "stage_names": {
            0: "चरण 0 — चारा (Bait)",
            1: "चरण 1 — विश्वास बनाना (Hook)",
            2: "चरण 2 — प्रीपेड जाल (Prepaid Trap)",
            3: "चरण 3 — पैसा फंसाना (Lock-in)",
            4: "चरण 4 — पलायन (Exit Scam)",
        },
        "stage_descriptions": {
            0: "स्कैमर बिना इंटरव्यू आसान काम के बदले भारी दैनिक वेतन का लालच देता है।",
            1: "विश्वास जीतने के लिए छोटा भुगतान (₹150-₹500) भेजा जाता है या टेलीग्राम ग्रुप में जोड़ा जाता है।",
            2: "अधिक मुनाफे का लालच देकर आपसे अपने पैसे जमा (डिपॉजिट) करने को कहा जाता है।",
            3: "पैसे की निकासी रोक दी जाती है और टैक्स या अनफ्रीज शुल्क के नाम पर और पैसे मांगे जाते हैं।",
            4: "ग्रुप डिलीट कर दिया जाता है, नंबर ब्लॉक हो जाता है, या फर्जी 'रिकवरी एजेंट' संपर्क करता है।",
        },
        "next_likely_moves": {
            0: "वे आपको टेलीग्राम या व्हाट्सएप ग्रुप में बुलाएंगे और विश्वास जीतने के लिए ₹100-₹200 का छोटा भुगतान करेंगे।",
            1: "वे आपसे 'वीआईपी टास्क' के लिए ₹1,000 से ₹5,000 किसी निजी यूपीआई पर जमा करने को कहेंगे और 30% मुनाफे का वादा करेंगे।",
            2: "पैसे भेजते ही वे कहेंगे कि 'सिस्टम एरर' हो गया है और निकासी के लिए ₹10,000 और जमा करने होंगे।",
            3: "वे टैक्स या पेनल्टी के नाम पर और पैसे मांगेंगे। बिल्कुल पैसे न दें — वे पैसे कभी वापस नहीं करेंगे।",
            4: "पैसे वापस दिलाने का दावा करने वाले फर्जी 'साइबर रिकवरी एजेंट' से सावधान रहें, यह दूसरा स्कैम है।",
        },
        "default_advice": {
            Verdict.SCAM: [
                "किसी भी हालत में कोई पैसा, रजिस्ट्रेशन फीस या सिक्योरिटी डिपॉजिट न भेजें।",
                "तुरंत सभी चैट, यूपीआई आईडी और बैंक खातों के स्क्रीनशॉट सुरक्षित कर लें।",
                "तुरंत राष्ट्रीय साइबर हेल्पलाइन 1930 पर कॉल करें ताकि आरोपी का बैंक खाता फ्रीज हो सके।",
                "सबूत सहेजने के बाद स्कैमर को व्हाट्सएप और टेलीग्राम पर ब्लॉक करें।",
            ],
            Verdict.SUSPICIOUS: [
                "नौकरी पाने के लिए कभी पैसे न दें। कोई भी असली कंपनी नौकरी देने के लिए पैसे नहीं मांगती।",
                "कंपनी का विवरण आधिकारिक MCA पोर्टल (mca.gov.in) पर अवश्य जांचें।",
                "टेलीग्राम के अज्ञात ग्रुप में न जुड़ें और अपना बैंक विवरण या ओटीपी कभी साझा न करें।",
            ],
            Verdict.LIKELY_GENUINE: [
                "यह प्रस्ताव सामान्य भर्ती प्रक्रिया जैसा प्रतीत होता है।",
                "फिर भी अपने दस्तावेज भेजने से पहले रिक्रूटर की आधिकारिक ईमेल आईडी अवश्य जांचें।",
                "किसी भी परिस्थिति में अपना बैंकिंग पासवर्ड या ओटीपी किसी के साथ साझा न करें।",
            ],
            Verdict.UNSURE: [
                "संदेश में पर्याप्त जानकारी उपलब्ध नहीं है।",
                "यदि वे किसी भी समय पैसे की मांग करें तो तुरंत बातचीत बंद कर दें।",
                "कंपनी की आधिकारिक वेबसाइट और ईमेल से सत्यापन की मांग करें।",
            ],
        },
    },
    "pa": {
        "verdict_labels": {
            Verdict.SCAM: "ਧੋਖਾਧੜੀ (ਸਕੈਮ) ਦੀ ਪੁਸ਼ਟੀ",
            Verdict.SUSPICIOUS: "ਸ਼ੱਕੀ / ਉੱਚ ਜੋਖਮ",
            Verdict.LIKELY_GENUINE: "ਅਸਲੀ ਹੋਣ ਦੀ ਸੰਭਾਵਨਾ",
            Verdict.UNSURE: "ਅਸਪਸ਼ਟ / ਸਾਵਧਾਨੀ ਵਰਤੋ",
        },
        "stage_names": {
            0: "ਪੜਾਅ 0 — ਚੋਗਾ (Bait)",
            1: "ਪੜਾਅ 1 — ਭਰੋਸਾ ਬਣਾਉਣਾ (Hook)",
            2: "ਪੜਾਅ 2 — ਪ੍ਰੀਪੇਡ ਜਾਲ (Prepaid Trap)",
            3: "ਪੜਾਅ 3 — ਪੈਸੇ ਫਸਾਉਣਾ (Lock-in)",
            4: "ਪੜਾਅ 4 — ਭੱਜ ਜਾਣਾ (Exit Scam)",
        },
        "stage_descriptions": {
            0: "ਸਕੈਮਰ ਬਿਨਾਂ ਇੰਟਰਵਿਊ ਦੇ ਸੌਖੇ ਕੰਮ ਬਦਲੇ ਮੋਟੀ ਰਕਮ ਕਮਾਉਣ ਦਾ ਲਾਲਚ ਦਿੰਦਾ ਹੈ।",
            1: "ਭਰੋਸਾ ਜਿੱਤਣ ਲਈ ਛੋਟਾ ਭੁਗਤਾਨ (₹150-₹500) ਦਿੱਤਾ ਜਾਂਦਾ ਹੈ।",
            2: "ਵਧੇਰੇ ਮੁਨਾਫੇ ਦਾ ਝਾਂਸਾ ਦੇ ਕੇ ਤੁਹਾਡੇ ਕੋਲੋਂ ਪੈਸੇ ਜਮ੍ਹਾਂ (ਡਿਪਾਜ਼ਿਟ) ਕਰਵਾਏ ਜਾਂਦੇ ਹਨ।",
            3: "ਪੈਸੇ ਕਢਵਾਉਣ 'ਤੇ ਰੋਕ ਲਗਾ ਕੇ ਟੈਕਸ ਜਾਂ ਜੁਰਮਾਨੇ ਦੇ ਨਾਂ 'ਤੇ ਹੋਰ ਪੈਸੇ ਮੰਗੇ ਜਾਂਦੇ ਹਨ।",
            4: "ਗਰੁੱਪ ਡਿਲੀਟ ਹੋ ਜਾਂਦਾ ਹੈ, ਨੰਬਰ ਬਲਾਕ ਹੋ ਜਾਂਦਾ ਹੈ, ਜਾਂ ਫਰਜ਼ੀ 'ਰਿਕਵਰੀ ਏਜੰਟ' ਸੰਪਰਕ ਕਰਦਾ ਹੈ।",
        },
        "next_likely_moves": {
            0: "ਉਹ ਤੁਹਾਨੂੰ ਟੈਲੀਗ੍ਰਾਮ 'ਤੇ ਬੁਲਾਉਣਗੇ ਅਤੇ ਭਰੋਸਾ ਜਿੱਤਣ ਲਈ ₹100-₹200 ਦਾ ਛੋਟਾ ਭੁਗਤਾਨ ਕਰਨਗੇ।",
            1: "ਉਹ ਤੁਹਾਨੂੰ ਵੀਆਈਪੀ ਟਾਸਕ ਲਈ ₹1,000 ਤੋਂ ₹5,000 ਯੂਪੀਆਈ 'ਤੇ ਜਮ੍ਹਾਂ ਕਰਨ ਲਈ ਕਹਿਣਗੇ।",
            2: "ਪੈਸੇ ਭੇਜਣ ਤੋਂ ਬਾਅਦ ਉਹ ਕਹਿਣਗੇ ਕਿ ਕੰਮ ਗਲਤ ਹੋ ਗਿਆ ਅਤੇ ₹10,000 ਹੋਰ ਮੰਗਣਗੇ।",
            3: "ਉਹ ਟੈਕਸ ਜਾਂ ਅਨਫ੍ਰੀਜ਼ ਫੀਸ ਦੇ ਨਾਂ 'ਤੇ ਹੋਰ ਪੈਸੇ ਮੰਗਣਗੇ। ਬਿਲਕੁਲ ਪੈਸੇ ਨਾ ਦਿਓ।",
            4: "ਪੈਸੇ ਵਾਪਸ ਕਰਵਾਉਣ ਦੇ ਨਾਂ 'ਤੇ ਪੈਸੇ ਮੰਗਣ ਵਾਲੇ ਫਰਜ਼ੀ ਰਿਕਵਰੀ ਏਜੰਟਾਂ ਤੋਂ ਸਾਵਧਾਨ ਰਹੋ।",
        },
        "default_advice": {
            Verdict.SCAM: [
                "ਕਿਸੇ ਵੀ ਹਾਲਤ ਵਿੱਚ ਕੋਈ ਪੈਸਾ, ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਫੀਸ ਜਾਂ ਡਿਪਾਜ਼ਿਟ ਨਾ ਭੇਜੋ।",
                "ਸਾਰੀਆਂ ਚੈਟਾਂ, ਯੂਪੀਆਈ ਆਈਡੀ ਅਤੇ ਬੈਂਕ ਖਾਤਿਆਂ ਦੇ ਸਕ੍ਰੀਨਸ਼ੌਟ ਤੁਰੰਤ ਸੁਰੱਖਿਅਤ ਕਰੋ।",
                "ਤੁਰੰਤ ਰਾਸ਼ਟਰੀ ਸਾਈਬਰ ਕ੍ਰਾਈਮ ਹੈਲਪਲਾਈਨ 1930 'ਤੇ ਕਾਲ ਕਰਕੇ ਸ਼ਿਕਾਇਤ ਦਰਜ ਕਰੋ।",
                "ਸਬੂਤ ਸਾਂਭਣ ਤੋਂ ਬਾਅਦ ਸਕੈਮਰ ਨੂੰ ਵਟਸਐਪ ਅਤੇ ਟੈਲੀਗ੍ਰਾਮ 'ਤੇ ਬਲਾਕ ਕਰੋ।",
            ],
            Verdict.SUSPICIOUS: [
                "ਨੌਕਰੀ ਲੈਣ ਲਈ ਕਦੇ ਪੈਸੇ ਨਾ ਦਿਓ। ਕੋਈ ਵੀ ਅਸਲੀ ਕੰਪਨੀ ਨੌਕਰੀ ਬਦਲੇ ਪੈਸੇ ਨਹੀਂ ਮੰਗਦੀ।",
                "ਕੰਪਨੀ ਦੇ ਅਧਿਕਾਰਤ ਪੋਰਟਲ (mca.gov.in) ਤੋਂ ਪੁਸ਼ਟੀ ਜ਼ਰੂਰ ਕਰੋ।",
                "ਆਪਣਾ ਬੈਂਕ ਵੇਰਵਾ, ਓਟੀਪੀ ਜਾਂ ਆਧਾਰ ਕਾਰਡ ਕਿਸੇ ਨਾਲ ਸਾਂਝਾ ਨਾ ਕਰੋ।",
            ],
            Verdict.LIKELY_GENUINE: [
                "ਇਹ ਪੇਸ਼ਕਸ਼ ਆਮ ਨੌਕਰੀ ਦੀ ਭਰਤੀ ਪ੍ਰਕਿਰਿਆ ਵਰਗੀ ਜਾਪਦੀ ਹੈ।",
                "ਫਿਰ ਵੀ ਆਪਣੇ ਦਸਤਾਵੇਜ਼ ਭੇਜਣ ਤੋਂ ਪਹਿਲਾਂ ਕੰਪਨੀ ਦੇ ਅਧਿਕਾਰਤ ਈਮੇਲ ਤੋਂ ਤਸਦੀਕ ਕਰੋ।",
                "ਆਪਣਾ ਬੈਂਕਿੰਗ ਪਾਸਵਰਡ ਜਾਂ ਓਟੀਪੀ ਕਦੇ ਵੀ ਕਿਸੇ ਨਾਲ ਸਾਂਝਾ ਨਾ ਕਰੋ।",
            ],
            Verdict.UNSURE: [
                "ਸੁਨੇਹੇ ਵਿੱਚ ਕਾਫ਼ੀ ਜਾਣਕਾਰੀ ਉਪਲਬਧ ਨਹੀਂ ਹੈ।",
                "ਜੇਕਰ ਉਹ ਕਦੇ ਵੀ ਪੈਸੇ ਦੀ ਮੰਗ ਕਰਦੇ ਹਨ, ਤਾਂ ਤੁਰੰਤ ਗੱਲਬਾਤ ਬੰਦ ਕਰੋ।",
                "ਕੰਪਨੀ ਦੀ ਅਧਿਕਾਰਤ ਵੈੱਬਸਾਈਟ ਤੋਂ ਪੁਸ਼ਟੀ ਕਰੋ।",
            ],
        },
    },
}


def get_localized_pack(lang: str) -> dict[str, Any]:
    return TRANSLATIONS.get(lang.lower(), TRANSLATIONS["en"])


def get_localized_advice(verdict: Verdict, lang: str) -> list[str]:
    pack = get_localized_pack(lang)
    return pack["default_advice"].get(verdict, pack["default_advice"][Verdict.UNSURE])


def get_localized_next_move(stage: int, lang: str) -> str:
    pack = get_localized_pack(lang)
    return pack["next_likely_moves"].get(stage, pack["next_likely_moves"][0])


def get_localized_stage_label(stage: int, lang: str) -> str:
    pack = get_localized_pack(lang)
    return pack["stage_names"].get(stage, f"Stage {stage}")
