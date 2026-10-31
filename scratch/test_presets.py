import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

presets = [
    ('demo-hook', 'YouTube Like Scam (Trial 150)', '''[29/10/2026, 11:00 AM] @Priya_HR: Welcome to Taskforce Digital E-Services! I am your mentor.
[29/10/2026, 11:01 AM] @Priya_HR: Here is Task 1: Open this link, like the video and send screenshot. You will get Rs 150 trial bonus.
[29/10/2026, 11:05 AM] User: Done, sent screenshot of liked video.
[29/10/2026, 11:06 AM] @Priya_HR: Send your UPI ID or GPay number to receive payment.
[29/10/2026, 11:07 AM] User: myupi99@oksbi
[29/10/2026, 11:10 AM] @Priya_HR: Rs 150 has been credited to your account! Please check your bank SMS.
[29/10/2026, 11:11 AM] User: Yes got Rs 150! Thank you!
[29/10/2026, 11:12 AM] @Priya_HR: Great! Adding you to our VIP Task Channel. We have merchant commission tasks coming up.'''),

    ('demo-prepaid', 'Prepaid Task Scam (Deposit 1000)', '''[30/10/2026, 12:00 PM] Mentor Rohit: You have completed novice tasks. Now starting Merchant Prepaid Task.
[30/10/2026, 12:01 PM] Mentor Rohit: Package A: Deposit Rs 1,000 -> Return Rs 1,300 within 15 minutes.
[30/10/2026, 12:01 PM] Mentor Rohit: Package B: Deposit Rs 5,000 -> Return Rs 6,800.
[30/10/2026, 12:02 PM] User: Why do I have to deposit my own money? This was supposed to be a job.
[30/10/2026, 12:03 PM] Mentor Rohit: This is a merchant security deposit to place mock orders. The money is 100% safe and refunded with 30% profit immediately.
[30/10/2026, 12:04 PM] Mentor Rohit: Pay Rs 1,000 to merchant UPI ID: rajeshkumar8472@ybl and send screenshot immediately. Only 2 slots left!'''),

    ('demo-lockin', 'Frozen Withdrawal (Tax Demand 58k)', '''[30/10/2026, 04:30 PM] User: I tried to withdraw my balance of Rs 1,54,000 from the platform but it says WITHDRAWAL FROZEN. Please help!
[30/10/2026, 04:32 PM] Finance Dept: Sir, your account has triggered anti-money laundering audit. As per Indian Income Tax regulations, you must pay 18% GST and 20% TDS (Rs 58,520) before withdrawal can be approved.
[30/10/2026, 04:34 PM] User: Can't you just deduct the tax from my Rs 1.54 Lakh balance and give me the rest?
[30/10/2026, 04:35 PM] Finance Dept: No, the system cannot deduct automatically. You must deposit Rs 58,520 from your own bank account to our clearing account within 2 hours or your account will be permanently frozen and reported to police!'''),

    ('demo-genuine', 'Genuine Offer (Infosys)', '''INFOSYS LIMITED
CIN: L85110KA1981PLC013115
Electronic City, Hosur Road, Bangalore - 560100
Date: October 15, 2026
Dear Student,
Sub: Offer of Employment - Systems Engineer
Further to our campus recruitment drive and subsequent technical & HR interviews conducted on October 5, 2026, we are pleased to offer you the role of Systems Engineer.
Annual Gross Salary: INR 3,60,000 per annum.
Please note:
- Infosys does not charge any application, processing, or training fee at any stage of recruitment.
- Please verify your offer letter on our official portal: https://career.infosys.com
- Your official reporting date is January 12, 2027 at Infosys Mysore Campus.
Warm regards,
HR Recruitment Team, Infosys Limited
recruitment@infosys.com''')
]

for pid, name, text in presets:
    req = urllib.request.Request(
        'http://localhost:8000/api/analyze',
        data=json.dumps({'raw_text': text}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        d = json.loads(resp.read().decode('utf-8'))
        v = d.get('verdict')
        rs = d.get('risk_score')
        st = d.get('stage')
        sig = len(d.get('signals', []))
        print(f"{name} -> Verdict: {v} | Risk Score: {rs} | Stage: {st} | Signals: {sig}")
