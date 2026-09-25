"""Stage the editable cv.yaml and generated artifacts for Jekyll.

Run after `python cv/generate_cv.py`, before the Jekyll build.
"""
from pathlib import Path
from shutil import copy2, copytree
import sys

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "cv"))
from generate_cv import load_cv  # noqa: E402


def main():
    data = load_cv()
    docs = REPO / "docs"
    data_path = docs / "_data" / "cv.yml"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    copy2(REPO / "cv.yaml", data_path)
    assets = docs / "assets" / "cv"
    assets.mkdir(parents=True, exist_ok=True)
    copy2(REPO / "cv" / "Kajal_Kale_CV.pdf", assets / "Kajal_Kale_CV.pdf")
    copytree(REPO / "cv" / "diagrams", assets / "diagrams", dirs_exist_ok=True)
    # Pages contain only stable slugs. Their visible copy comes from cv.yaml via site.data.cv.
    for project in data["projects"]:
        slug = project["slug"]
        page = docs / "projects" / f"{slug}.md"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(f"---\nlayout: project\nsource: {slug}\npermalink: /projects/{slug}/\n---\n", encoding="utf-8")
    print(f"Staged {len(data['projects'])} project pages and CV assets for Jekyll")


if __name__ == "__main__":
    main()
