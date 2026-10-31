import dulwich.porcelain as p

repo_path = "."

# Files to stage
files_to_add = [
    "README.md",
    "frontend/README.md",
    "backend/README.md",
    "backend/app/modules/README.md",
    "backend/app/modules/job_task_classifier/README.md",
    "backend/app/modules/company_verification/README.md",
    "backend/app/modules/conversation_intelligence/README.md",
    "backend/app/modules/scam_stage_identification/README.md",
    "backend/app/modules/victim_protection/README.md",
    "modules_zips/job_task_classifier.zip",
    "modules_zips/company_verification.zip",
    "modules_zips/conversation_intelligence.zip",
    "modules_zips/scam_stage_identification.zip",
    "modules_zips/victim_protection.zip",
    "modules_zips/evaluation_benchmark.zip",
    "modules_zips/frontend_src.zip",
]

p.add(repo_path, files_to_add)

commit_msg = b"docs: overhaul root, client, server, and modular READMEs to match Storage-App standard"
commit_id = p.commit(repo_path, message=commit_msg, author=b"OfferGuard Team <team@offerguard.ai>")

print("Committed successfully!")
print("Commit Hash:", commit_id.decode("utf-8") if isinstance(commit_id, bytes) else commit_id)
