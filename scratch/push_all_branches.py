import sys
import dulwich.porcelain as p

if len(sys.argv) < 2:
    print("Usage: python scratch/push_all_branches.py <YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>")
    sys.exit(1)

token = sys.argv[1].strip()
repo_url = f"https://{token}@github.com/mydestinyistrue/offerguard-ai.git"

branches = [
    "main",
    "job-task-classifier",
    "company-verification",
    "conversation_intelligence",
    "scam_stage_identification",
    "victim-protection",
]

for b in branches:
    ref = f"refs/heads/{b}"
    print(f"Pushing {b} to {repo_url[:20]}... -> {ref}")
    try:
        p.push(".", repo_url, ref)
        print(f"  ✓ {b} pushed successfully!")
    except Exception as e:
        print(f"  ✗ Error pushing {b}: {e}")

print("Push operations completed!")
