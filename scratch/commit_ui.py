import os
import dulwich.porcelain as porcelain
from dulwich.repo import Repo

repo_path = r"c:\Users\Atul kaushal\Downloads\offergaurd-ai"
repo = Repo(repo_path)

status = porcelain.status(repo_path)
print("Untracked:", status.untracked)
print("Staged:", status.staged)
print("Unstaged:", status.unstaged)

# Add all modified and untracked files in frontend/src
porcelain.add(repo_path, paths=[
    "frontend/src/index.css",
    "frontend/src/components/Navbar.jsx",
    "frontend/src/components/Footer.jsx",
    "frontend/src/components/VerdictBanner.jsx",
    "frontend/src/components/EvidenceCard.jsx",
    "frontend/src/components/CompanyCheck.jsx",
    "frontend/src/components/NextMoveCard.jsx",
    "frontend/src/components/StageTimeline.jsx",
    "frontend/src/components/ReportPack.jsx",
    "frontend/src/components/AdviceSection.jsx",
    "frontend/src/pages/HomePage.jsx",
    "frontend/src/pages/AboutPage.jsx",
    "frontend/src/pages/PrivacyPage.jsx",
    "frontend/src/pages/EvalPage.jsx",
])

commit_id = porcelain.commit(
    repo_path,
    message=b"Refine UI: remove agentic badges and jargon, polish button padding and clean_design styles"
)
print("Committed successfully:", commit_id.decode())
