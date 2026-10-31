import os
import sys
import tempfile
import zipfile
from pathlib import Path

# Create an isolated temporary directory
temp_dir = Path(tempfile.mkdtemp(prefix="test_extracted_modules_"))
print("Testing extraction into:", temp_dir)

zips = [
    Path(r"c:\Users\Atul kaushal\Downloads\offergaurd-ai\modules_zips\job_task_classifier.zip"),
    Path(r"c:\Users\Atul kaushal\Downloads\offergaurd-ai\modules_zips\company_verification.zip"),
    Path(r"c:\Users\Atul kaushal\Downloads\offergaurd-ai\modules_zips\conversation_intelligence.zip"),
    Path(r"c:\Users\Atul kaushal\Downloads\offergaurd-ai\modules_zips\scam_stage_identification.zip"),
    Path(r"c:\Users\Atul kaushal\Downloads\offergaurd-ai\modules_zips\victim_protection.zip"),
]

# Extract all 5 zips into temp_dir
for z in zips:
    with zipfile.ZipFile(z, "r") as zf:
        zf.extractall(temp_dir)
        print(f"Extracted {z.name}")

# Add temp_dir to the FRONT of sys.path, and remove any references to offergaurd-ai
sys.path.insert(0, str(temp_dir))
sys.path = [p for p in sys.path if "offergaurd-ai" not in p.lower() or p == str(temp_dir)]

print("\n--- Testing Module 1: job_task_classifier ---")
from job_task_classifier import JobTaskClassifier, classify_job_offer
clf = JobTaskClassifier()
res1 = clf.classify("Deposit Rs 1000 to get Rs 1500 return within 15 minutes")
print("Module 1 OK! Verdict:", res1.verdict, "Risk:", res1.risk_score)

print("\n--- Testing Module 2: company_verification ---")
from company_verification import CompanyVerifier, MCALookupService
cv = CompanyVerifier()
res2 = cv.verify(company_name="Infosys Limited", text="Official recruitment at Infosys Limited")
print("Module 2 OK! Company:", res2.company_name, "MCA Verified:", res2.mca_verified, "Outcome:", res2.verification_outcome)

print("\n--- Testing Module 3: conversation_intelligence ---")
from conversation_intelligence import ConversationPipeline, mask_pii
cp = ConversationPipeline()
res3 = cp.process("[10:00 AM] Recruiter: Hello call 9876543210 for VIP job")
print("Module 3 OK! Messages parsed:", len(res3.messages), "PII Found:", res3.pii_found)

print("\n--- Testing Module 4: scam_stage_identification ---")
from scam_stage_identification import ScamStageClassifier, ScamStageEngine
sc = ScamStageClassifier()
res4 = sc.identify_stage("Pay 5000 rs deposit for merchant task commission")
print("Module 4 OK! Stage:", res4.stage, res4.stage_name)

print("\n--- Testing Module 5: victim_protection ---")
from victim_protection import ReportGenerator, get_localized_pack
rg = ReportGenerator()
res5 = rg.generate_complaint_pack(
    text="Paid 5000 to scammer via UPI rajesh@upi",
    victim_name="John Doe",
    amount_lost=5000.0,
    language="en"
)
print("Module 5 OK! Report generated with length:", len(res5.report_text))

print("\nSUCCESS! All 5 extracted modules imported and ran standalone with ZERO errors.")
