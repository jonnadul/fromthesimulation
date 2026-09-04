# From the Simulation — Jekyll blog

Migrated from Substack. Site source lives here; the generated site is in
`_site/` (git-ignored).

## Requirements

Ruby 3.4 was installed to `C:\Ruby34-x64`. The `jekyll` launcher script has a
path quirk on this box, so invoke Jekyll explicitly via `ruby`:

```bash
export PATH="/c/Ruby34-x64/bin:$PATH"
ruby C:/Ruby34-x64/bin/jekyll <command>
```

Or use the bundled wrappers (no PATH setup needed):

```bash
./serve.sh      # preview at http://127.0.0.1:4000  (auto-rebuilds on save)
./build.sh      # one-off build into _site/
```

## Writing

```bash
python tools/new_post.py "My Post Title" --subtitle "Optional"
```

Then edit the generated file in `_posts/`. Save and the local preview reloads.

Posts use `YYYY-MM-DD-slug.md` naming and standard YAML front matter.
Drafts go in `_drafts/` (no date prefix needed) and are not published.

## Layout

```
_posts/         blog posts (imported Substack content lives here)
_drafts/        unpublished drafts
_layouts/       default / post / page / home templates
assets/css/     stylesheet (light + dark, follows OS setting)
assets/img/raw/ post images, self-hosted (15 files migrated from Substack)
tools/          migration + authoring helpers
_site/          generated output (do not edit; git-ignored)
```

## Migration notes

Content came from a Substack export. `tools/substack_to_jekyll.py` converted
the HTML bodies to Markdown and rewrote all 15 remote image URLs to local
files, so the site has **zero** dependencies on Substack's CDN.

- 7 published posts migrated
- 1 empty draft preserved as `_drafts/untitled-draft-205723424.md`
- Subscriber list (31 emails) was **not** imported — it stays in your
  Downloads export and is deliberately excluded from the site.

## Deploying

`_site/` is static HTML. Push the repo to GitHub and enable GitHub Pages
(Settings → Pages → Deploy from branch), or upload `_site/` to any static host.
Set `url:` and `baseurl:` in `_config.yml` before deploying.
