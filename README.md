# LJT-Homepage

Junteng Liu's single-page academic homepage, forked from [Academic Pages](https://github.com/academicpages/academicpages.github.io).

## Content

All personal content is in the existing [`_pages/about.md`](_pages/about.md): background, research interests, education, research internships, all six publications, the Zhiyuan Honor Scholarship, and contact information. The content is limited to the supplied memory, including its dates and first-year PhD status. No technical skills, portrait, publication URLs, or additional personal details have been inferred.

Navigation uses anchors on the About page. The inherited example pages, posts, collections, sample files, and images are excluded from the build. No additional HTML pages, publication subpages, feeds, or redirects are generated. This README and the validation script are also excluded from the website.

The repository is hosted under `Mountainkuimplode`; the personal GitHub profile remains `Vicent0205`, as supplied in memory.

## Build and check

```sh
bundle install
bundle exec jekyll build
python3 scripts/validate_homepage.py
```

The GitHub Actions workflow builds the site and validates the single-page output, publications, contact links, and internal asset paths. It uploads the generated Pages artifact and deploys only when GitHub Pages is enabled with **GitHub Actions** as its source. Enabling Pages requires repository settings access; the workflow does not silently change that setting.

The configured project-site address is `https://mountainkuimplode.github.io/LJT-Homepage/`. Configuration alone does not make this address live. If Pages is disabled, choose **Settings → Pages → Build and deployment → Source: GitHub Actions**, then run the **Build and deploy LJT-Homepage** workflow.

The original theme's license is retained in `LICENSE`.
