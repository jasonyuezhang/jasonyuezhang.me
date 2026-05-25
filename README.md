# jasonyuezhang.me

Personal blog built with Jekyll and deployed to GitHub Pages with GitHub Actions.

## Local development

```bash
bundle install
bundle exec jekyll serve
```

Open <http://127.0.0.1:4000>.

## Publishing

Push to `main`. The Pages workflow builds the Jekyll site and deploys `_site` as a GitHub Pages artifact.

In the repository settings, set **Pages > Build and deployment > Source** to **GitHub Actions**.

## Comments

Comments use Giscus, which stores threads in GitHub Discussions. To enable them:

1. Make the repository public.
2. Enable GitHub Discussions for the repository.
3. Install the Giscus GitHub app for this repository.
4. Use <https://giscus.app> to generate the repository ID and category ID.
5. Add those values to `_config.yml` under `giscus` and set `enabled: true`.
