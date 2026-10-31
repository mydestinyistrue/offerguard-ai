"""Script to populate data/mca.sqlite with realistic MCA company master data."""

import sqlite3
import re
from pathlib import Path

def normalize_name(name: str) -> str:
    name = re.sub(r"[^\w\s]", "", name.lower())
    stopwords = ["pvt", "private", "ltd", "limited", "llp", "corp", "corporation", "inc", "co", "company", "india"]
    words = [w for w in name.split() if w not in stopwords]
    return " ".join(words)

companies = [
    # Top IT & Tech
    ("L72200MH1995PLC085699", "Tata Consultancy Services Limited", "Active", "RoC-Mumbai", "Company limited by Shares", "Non-govt company", "Public", "1995-01-19", "Maharashtra", 1000000000.0, 365905000.0, "corporate.compliance@tcs.com"),
    ("L85110KA1981PLC013115", "Infosys Limited", "Active", "RoC-Bangalore", "Company limited by Shares", "Non-govt company", "Public", "1981-07-02", "Karnataka", 2400000000.0, 2069000000.0, "investors@infosys.com"),
    ("L32102KA1945PLC020800", "Wipro Limited", "Active", "RoC-Bangalore", "Company limited by Shares", "Non-govt company", "Public", "1945-12-29", "Karnataka", 11000000000.0, 10480000000.0, "corp-secretarial@wipro.com"),
    ("L74140DL1991PLC046369", "HCL Technologies Limited", "Active", "RoC-Delhi", "Company limited by Shares", "Non-govt company", "Public", "1991-11-12", "Delhi", 600000000.0, 542000000.0, "investors@hcl.com"),
    ("L64200MH1986PLC041370", "Tech Mahindra Limited", "Active", "RoC-Mumbai", "Company limited by Shares", "Non-govt company", "Public", "1986-10-24", "Maharashtra", 5000000000.0, 4880000000.0, "investor.relations@techmahindra.com"),
    ("U72200KA2004PTC034233", "Google India Private Limited", "Active", "RoC-Bangalore", "Company limited by Shares", "Non-govt company", "Private", "2004-07-06", "Karnataka", 10000000.0, 10000000.0, "compliance-india@google.com"),
    ("U72900DL2005PTC138856", "Microsoft Corporation (India) Private Limited", "Active", "RoC-Delhi", "Company limited by Shares", "Non-govt company", "Private", "2005-07-19", "Delhi", 50000000.0, 25000000.0, "mscareer@microsoft.com"),
    ("U72200KA1996PTC020572", "Amazon Development Centre (India) Private Limited", "Active", "RoC-Bangalore", "Company limited by Shares", "Non-govt company", "Private", "1996-05-30", "Karnataka", 100000000.0, 95000000.0, "cs-india@amazon.com"),
    ("U51909KA2012PTC066107", "Flipkart Internet Private Limited", "Active", "RoC-Bangalore", "Company limited by Shares", "Non-govt company", "Private", "2012-10-01", "Karnataka", 500000000.0, 420000000.0, "compliance@flipkart.com"),
    ("U74900KA2015PTC080645", "Fashnear Technologies Private Limited", "Active", "RoC-Bangalore", "Company limited by Shares", "Non-govt company", "Private", "2015-06-03", "Karnataka", 150000000.0, 120000000.0, "legal@meesho.com"), # Meesho
    ("U72200DL2010PTC204636", "Bundl Technologies Private Limited", "Active", "RoC-Bangalore", "Company limited by Shares", "Non-govt company", "Private", "2010-06-22", "Karnataka", 300000000.0, 245000000.0, "support@swiggy.in"), # Swiggy
    ("L93030DL2010PLC198141", "Zomato Limited", "Active", "RoC-Delhi", "Company limited by Shares", "Non-govt company", "Public", "2010-01-18", "Delhi", 1000000000.0, 880000000.0, "companysecretary@zomato.com"),
    ("U74999HR2017PTC069904", "One97 Communications Limited", "Active", "RoC-Delhi", "Company limited by Shares", "Non-govt company", "Public", "2000-12-22", "Haryana", 1041000000.0, 635000000.0, "compliance@paytm.com"),
    
    # Conglomerates & Retail
    ("L17110MH1973PLC019786", "Reliance Industries Limited", "Active", "RoC-Mumbai", "Company limited by Shares", "Non-govt company", "Public", "1973-05-08", "Maharashtra", 150000000000.0, 67650000000.0, "investor.relations@ril.com"),
    ("U01100MH1999PTC120563", "Reliance Retail Limited", "Active", "RoC-Mumbai", "Company limited by Shares", "Non-govt company", "Public", "1999-06-24", "Maharashtra", 60000000000.0, 49870000000.0, "retail.compliance@ril.com"),
    ("L28920MH1945PLC004520", "Tata Motors Limited", "Active", "RoC-Mumbai", "Company limited by Shares", "Non-govt company", "Public", "1945-09-01", "Maharashtra", 8000000000.0, 7650000000.0, "inv_rel@tatamotors.com"),
    ("L27100MH1907PLC000260", "Tata Steel Limited", "Active", "RoC-Mumbai", "Company limited by Shares", "Non-govt company", "Public", "1907-08-26", "Maharashtra", 17500000000.0, 12220000000.0, "cosecretarial@tatasteel.com"),
    ("L15140MH1933PLC002030", "Hindustan Unilever Limited", "Active", "RoC-Mumbai", "Company limited by Shares", "Non-govt company", "Public", "1933-10-17", "Maharashtra", 2850000000.0, 2350000000.0, "levercare.shareholder@unilever.com"),
    ("L65190MH2004GOI148838", "State Bank of India", "Active", "RoC-Mumbai", "Company limited by Shares", "Govt company", "Public", "1955-07-01", "Maharashtra", 10000000000.0, 8920000000.0, "agmcustomer.lho@sbi.co.in"),
    ("L65110MH1994PLC080618", "HDFC Bank Limited", "Active", "RoC-Mumbai", "Company limited by Shares", "Non-govt company", "Public", "1994-08-30", "Maharashtra", 11900000000.0, 7610000000.0, "shareholder.grievances@hdfcbank.com"),
    ("L65190GJ1994PLC021012", "ICICI Bank Limited", "Active", "RoC-Ahmedabad", "Company limited by Shares", "Non-govt company", "Public", "1994-01-05", "Gujarat", 25000000000.0, 14000000000.0, "investor@icicibank.com"),

    # Common Task Scam Targets & Delivery/Media
    ("U74140MH2018PTC309812", "Star Digital Media Entertainment Private Limited", "Active", "RoC-Mumbai", "Company limited by Shares", "Non-govt company", "Private", "2018-05-14", "Maharashtra", 5000000.0, 1000000.0, "compliance@stardigital.in"),
    ("U72900DL2019PTC345678", "Global Rating & Review Services Private Limited", "Active", "RoC-Delhi", "Company limited by Shares", "Non-govt company", "Private", "2019-02-11", "Delhi", 2000000.0, 500000.0, "contact@globalrating.in"),
    ("U74999MH2016PTC288123", "Taskforce E-Services Private Limited", "Active", "RoC-Mumbai", "Company limited by Shares", "Non-govt company", "Private", "2016-11-20", "Maharashtra", 1000000.0, 200000.0, "admin@taskforceservices.com"),
    ("U72200PN2021PTC199876", "CloudWork Solutions India Private Limited", "Active", "RoC-Pune", "Company limited by Shares", "Non-govt company", "Private", "2021-04-12", "Maharashtra", 1500000.0, 500000.0, "hr@cloudworkindia.com"),
    ("U52100DL2022PTC400122", "SmartCart E-Commerce Private Limited", "Active", "RoC-Delhi", "Company limited by Shares", "Non-govt company", "Private", "2022-06-18", "Delhi", 5000000.0, 1000000.0, "support@smartcart.co.in"),

    # Known Impersonation / Suspicious / Struck-off entities
    ("U72900UP2017PTC091234", "Digital Task India Private Limited", "Strike Off", "RoC-Kanpur", "Company limited by Shares", "Non-govt company", "Private", "2017-03-15", "Uttar Pradesh", 100000.0, 100000.0, "contact@digitaltask.com"),
    ("U74999DL2020PTC368811", "Telegram Online Task Services Private Limited", "Strike Off", "RoC-Delhi", "Company limited by Shares", "Non-govt company", "Private", "2020-08-25", "Delhi", 100000.0, 100000.0, "info@tele-task.com"),
    ("U72900MH2021PTC355444", "YouTube Promotion Agency Private Limited", "Under Process of Striking Off", "RoC-Mumbai", "Company limited by Shares", "Non-govt company", "Private", "2021-02-18", "Maharashtra", 100000.0, 100000.0, "ytpromo@gmail.com"),
    ("U74999PB2019PTC049920", "Punjab Job Placement Services Private Limited", "Active", "RoC-Chandigarh", "Company limited by Shares", "Non-govt company", "Private", "2019-07-10", "Punjab", 1000000.0, 500000.0, "contact@punjabjobs.org"),
    ("U72200HR2020PTC085112", "CyberTask India Technologies Private Limited", "Amalgamated", "RoC-Delhi", "Company limited by Shares", "Non-govt company", "Private", "2020-01-14", "Haryana", 2500000.0, 1200000.0, "legal@cybertask.in"),

    # Educational & Placement firms
    ("U80302DL2018PTC333444", "CT Institute of Technology Private Limited", "Active", "RoC-Delhi", "Company limited by Shares", "Non-govt company", "Private", "2018-04-12", "Delhi", 5000000.0, 2000000.0, "info@ctgroup.in"),
    ("U80903PB2015PTC039888", "BuildFest Innovations Private Limited", "Active", "RoC-Chandigarh", "Company limited by Shares", "Non-govt company", "Private", "2015-09-08", "Punjab", 2000000.0, 1000000.0, "connect@buildfest.org"),
    ("U74999DL2014PTC265432", "Naukri Internet Services Private Limited", "Active", "RoC-Delhi", "Company limited by Shares", "Non-govt company", "Private", "2014-03-21", "Delhi", 10000000.0, 8000000.0, "legal@naukri.com"),
    ("U72900KA2016PTC095123", "Internshala EduTech Private Limited", "Active", "RoC-Bangalore", "Company limited by Shares", "Non-govt company", "Private", "2016-07-28", "Karnataka", 15000000.0, 11000000.0, "careers@internshala.com"),
]

# Generate additional diverse companies across Indian states
states_roc = [
    ("Maharashtra", "RoC-Mumbai", "MH"),
    ("Delhi", "RoC-Delhi", "DL"),
    ("Karnataka", "RoC-Bangalore", "KA"),
    ("Punjab", "RoC-Chandigarh", "PB"),
    ("Haryana", "RoC-Delhi", "HR"),
    ("Gujarat", "RoC-Ahmedabad", "GJ"),
    ("Tamil Nadu", "RoC-Chennai", "TN"),
    ("Telangana", "RoC-Hyderabad", "TG"),
    ("West Bengal", "RoC-Kolkata", "WB"),
    ("Uttar Pradesh", "RoC-Kanpur", "UP"),
]

sectors = [
    ("Software Solutions", "72200", "PTC"),
    ("Digital Marketing", "74300", "PTC"),
    ("Logistics & Express", "63090", "PLC"),
    ("E-Commerce Ventures", "52599", "PTC"),
    ("Financial Consultancy", "67120", "PLC"),
    ("Healthcare & Pharma", "24239", "PLC"),
    ("Education Network", "80301", "PTC"),
    ("Hospitality Services", "55101", "PTC"),
]

prefixes = ["Apex", "Zenith", "Bharat", "Skyline", "Vanguard", "Pinnacle", "Indus", "Aura", "Nova", "Paramount", "Horizon", "Sunrise", "Global", "NextGen", "Quantum", "Synergy", "Vertex", "Omega"]

id_counter = 1000
for state, roc, code in states_roc:
    for prefix in prefixes:
        sec_name, nic, ctype = sectors[hash(prefix + state) % len(sectors)]
        year = 2000 + (hash(prefix + state + roc) % 24)
        cin = f"U{nic}{code}{year}{ctype}{id_counter}"
        cname = f"{prefix} {sec_name} Private Limited"
        cap = float((hash(cname) % 50 + 1) * 1000000)
        paid = float(cap * 0.75)
        status = "Active" if (id_counter % 7 != 0) else "Strike Off"
        email = f"info@{prefix.lower()}{code.lower()}.co.in"
        companies.append((
            cin, cname, status, roc, "Company limited by Shares", "Non-govt company",
            "Private" if ctype == "PTC" else "Public", f"{year}-0{(id_counter % 9)+1}-15",
            state, cap, paid, email
        ))
        id_counter += 1

db_path = Path("data/mca.sqlite")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

inserted = 0
for comp in companies:
    cin, name, status, roc, cat, sub_cat, cls, reg_date, state, auth_cap, paid_cap, email = comp
    norm_name = normalize_name(name)
    try:
        cur.execute("""
            INSERT OR REPLACE INTO companies 
            (cin, company_name, company_name_normalized, status, roc, category, sub_category, class, date_of_registration, state, authorized_capital, paid_up_capital, email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cin, name, norm_name, status, roc, cat, sub_cat, cls, reg_date, state, auth_cap, paid_cap, email))
        inserted += 1
    except Exception as e:
        print(f"Error inserting {name}: {e}")

conn.commit()
conn.close()
print(f"Successfully populated {inserted} MCA companies into data/mca.sqlite")
