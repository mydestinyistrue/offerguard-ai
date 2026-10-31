"""Push local Git commits and branches to GitHub using Dulwich.

Usage:
  python scripts/push_to_github.py <GITHUB_TOKEN> [BRANCH_NAME]
"""

import sys
import dulwich.porcelain as porcelain

def push_repo(token: str, branch: str = "feat/scam-stage-radar-ocr"):
    repo_path = "."
    r = porcelain.open_repo(repo_path)
    
    remote_url = f"https://{token}@github.com/mydestinyistrue/offerguard-ai.git"
    ref_name = f"refs/heads/{branch}"
    
    print(f"Pushing branch '{branch}' to https://github.com/mydestinyistrue/offerguard-ai.git...")
    try:
        porcelain.push(r, remote_url, ref_name)
        print("✓ Branch successfully pushed to GitHub!")
        print(f"View branch on GitHub: https://github.com/mydestinyistrue/offerguard-ai/tree/{branch}")
    except Exception as e:
        print(f"✗ Push failed: {e}")
        print("\nPlease ensure your GitHub Personal Access Token has 'repo' (write) scope.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/push_to_github.py <GITHUB_TOKEN> [BRANCH_NAME]")
        sys.exit(1)
    
    tok = sys.argv[1].strip()
    br = sys.argv[2].strip() if len(sys.argv) > 2 else "feat/scam-stage-radar-ocr"
    push_repo(tok, br)
