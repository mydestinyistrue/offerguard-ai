import os

commit_hash = "bbedff19df2f9507093b1e2ba01a166add5e7d8a"

branches = [
    "main",
    "job-task-classifier",
    "company-verification",
    "conversation_intelligence",
    "scam_stage_identification",
    "victim-protection",
]

heads_dir = os.path.abspath(".git/refs/heads")
for b in branches:
    p = os.path.join(heads_dir, b)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(commit_hash + "\n")
    print(f"Updated branch '{b}' -> {commit_hash[:8]}")

print("All branches synchronized locally!")
