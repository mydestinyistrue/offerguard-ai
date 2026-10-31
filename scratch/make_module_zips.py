import os
import shutil
import zipfile
from pathlib import Path

base_dir = Path(r"c:\Users\Atul kaushal\Downloads\offergaurd-ai")
modules_dir = base_dir / "backend" / "app" / "modules"
out_dir = base_dir / "modules_zips"
out_dir.mkdir(parents=True, exist_ok=True)

modules = [
    "job_task_classifier",
    "company_verification",
    "conversation_intelligence",
    "scam_stage_identification",
    "victim_protection",
]

# Ensure company_verification has data/mca.sqlite packaged
mca_src = base_dir / "backend" / "data" / "mca.sqlite"
mca_dst_dir = modules_dir / "company_verification" / "data"
mca_dst_dir.mkdir(parents=True, exist_ok=True)
if mca_src.exists():
    shutil.copy2(mca_src, mca_dst_dir / "mca.sqlite")
    print(f"Copied {mca_src} to {mca_dst_dir / 'mca.sqlite'}")

created_zips = []
for mod in modules:
    mod_path = modules_dir / mod
    zip_path = out_dir / f"{mod}.zip"
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(mod_path):
            # Skip __pycache__
            if "__pycache__" in root:
                continue
            for f in files:
                if f.endswith(".pyc"):
                    continue
                file_full = Path(root) / f
                # Relative path inside the zip file (starts with the module folder name)
                arc_name = file_full.relative_to(modules_dir)
                zf.write(file_full, arc_name)
    
    size_kb = zip_path.stat().st_size / 1024
    print(f"Created {zip_path.name} ({size_kb:.1f} KB)")
    created_zips.append(zip_path)

# Also copy zips to project root for easy access
root_zips_dir = base_dir / "exported_modules"
root_zips_dir.mkdir(parents=True, exist_ok=True)
for zp in created_zips:
    shutil.copy2(zp, root_zips_dir / zp.name)
    shutil.copy2(zp, base_dir / zp.name)

print("\nDone! All 5 module zips created successfully.")
