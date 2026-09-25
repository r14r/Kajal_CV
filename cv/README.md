# Editable CV and project portfolio

Edit **`cv.yaml` at the repository root**. It is the only source of CV text, project descriptions, architecture nodes and data flow steps used for the seven-page PDF, the HTML CV and the Jekyll website. The initial content is draft sample data. Leave unverified contact and education fields empty; only record Kajal's own, demonstrable project contributions.

## YAML structure

- `schema_version`: keep `1`.
- `cv`: name, subtitle, `contact` (email, city and GitHub profile), profile, `education` (degree, institution and dates), notes, draft flag and repository URL.
- `site`: page title, descriptions and hero and about text.
- `projects`: six entries with a stable slug, navigation information, summary, detailed implementation, file list, four architecture nodes and five data flow steps.

`slug` must match its folder under `projects/`. The current PDF design has a page per project and requires six projects, up to four file descriptions per project, four architecture nodes and five flow steps. The generator validates these constraints and stops on invalid YAML. Keep text concise enough for an A4 page. To expand the layout or add projects, update the generator and its validation.

## Build locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r cv/requirements.txt
python cv/generate_cv.py
python scripts/prepare_site.py
```

This updates `cv/Kajal_Kale_CV.html`, `cv/Kajal_Kale_CV.pdf`, all twelve SVGs under `cv/diagrams/`, and the Jekyll data, pages and assets under `docs/`. For the website, build with `jekyll build --source docs --destination _site` or follow `docs/README.md`.

On every push to `main`, `.github/workflows/pages.yml` regenerates these files from `cv.yaml`, builds the Jekyll site and deploys it to GitHub Pages. A merge into `main` is a push and triggers the same workflow. GitHub Pages must be configured with **GitHub Actions** as the source. The PDF may be downloaded independently; the HTML needs its sibling `diagrams/` folder.

These are prepared learning examples, not claims of employment or independent authorship. Kajal should inspect, run and modify them and describe only her own contributions.
