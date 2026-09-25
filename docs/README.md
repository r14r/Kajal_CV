# Jekyll portfolio website

The repository root `cv.yaml` is the editable source for the CV, home page, project navigation and six detailed project pages. The site keeps its Jekyll layout and animation under `docs/`; `scripts/prepare_site.py` stages YAML into `docs/_data/cv.yml`, generated PDF and SVG diagrams into `docs/assets/cv/`, and project page entry files into `docs/projects/`. Edit `cv.yaml` rather than these generated copies.

## Publish automatically

In repository **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source. `.github/workflows/pages.yml` runs on every push to `main`, including merges, and may also be started manually from the Actions tab. It regenerates the CV and data, builds Jekyll and deploys the Pages artifact. A push to another branch does not replace the live website. The project URL is `https://r14r.github.io/Kajal_CV/` once Pages is enabled. Availability for private repositories depends on the account plan; a published Pages site can be public even if its source repository is private. Review the draft CV before enabling public publishing.

## Edit and preview

Update `cv.yaml` and regenerate as described in `cv/README.md`. For a local website preview, after installing Ruby/Jekyll run:

```bash
python cv/generate_cv.py
python scripts/prepare_site.py
jekyll serve --source docs --baseurl /Kajal_CV
```

The Jekyll site is static: the Streamlit, Django, FastAPI and Ollama apps run separately as described in their own READMEs. Site navigation and internal links use `relative_url` to support the `/Kajal_CV/` base path.
