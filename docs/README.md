# Jekyll portfolio website

This folder is the GitHub Pages source for the `Kajal_CV` repository. It has a custom Jekyll layout, animated home hero, responsive sidebar, and six project detail pages. The site describes the projects as learning examples, with no invented work history or contact details.

## Publish from GitHub Pages

In repository **Settings → Pages → Build and deployment**, select **Deploy from a branch**, then **main** and **/docs**, and save. The configured project URL is `https://r14r.github.io/Kajal_CV/`. Pages availability for a private repository depends on the account plan; check the Pages settings before changing repository visibility. Publishing a Pages site can make the website publicly accessible even when source code is private. Review the content before enabling it.

## Edit

- `_config.yml`: site URL, `baseurl` and metadata.
- `_data/projects.yml`: sidebar links and project cards.
- `_layouts/default.html`: shared navigation and footer.
- `_layouts/project.html`: common project detail view.
- `index.html`: hero and overview.
- `projects/*.md`: detail pages.
- `assets/css/site.css` and `assets/js/site.js`: styling, responsive navigation and animation.

Use `relative_url` for internal links, so the site works at `/Kajal_CV/`. If the repository name changes, update `baseurl`.

## Local preview

With Ruby and Jekyll installed, run `jekyll serve --source docs --baseurl /Kajal_CV` from the repository root and open the URL printed by Jekyll. The site does not require third-party themes or plugins. Optional Google Fonts fall back to system fonts offline.

The GitHub Pages site is static: Streamlit, Django, FastAPI and Ollama projects are documented here, but their backends must be run separately as described in their own READMEs.
