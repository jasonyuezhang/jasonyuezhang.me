## Cursor Cloud specific instructions

This is a Jekyll 4.4.1 blog deployed to GitHub Pages.

### Key commands

- Dev: `bundle exec jekyll serve` (port 4000)
- Build: `bundle exec jekyll build`
- Install deps: `bundle install`

### Gotchas

- `.ruby-version` pins Ruby 4.0.5 but system Ruby 3.2.3 works fine for local development.
- Bundle path is configured locally to `vendor/bundle` (via `.bundle/config`). This directory is gitignored.
- Sass deprecation warnings about `lighten()` in minima theme are cosmetic and not actionable (comes from the theme gem).
