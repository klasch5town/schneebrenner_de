Schneebrenner Homepage Repository
=================================

This is a repository hosting the source for my homepage at https://www.schneebrenner.de.

I started to create my homepage with the help of the static site generator [pelican](https://getpelican.com/) in order
to get rid of Wordpress as this is immoderate for a small private homepage.
As building the statice site with Pelican process also includes a build-step (like in software development)
and as I'm used to repositories as an software developer I decided to store the 'homepage sources' at github.

Further advantages are that I can track the changes and have it stored not just at my server and local computer (a kind of backup).

May be at the end this repository is not just handy for me but will also show how to setup a homepage with pelican - means beyond the quick start example.

## Setup

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python 3.10+.

```bash
uv sync
```

## Local preview

Build and open the site in the browser:

```bash
uv run invoke reserve
```

Or, with auto-reload on file changes (recommended for editing):

```bash
uv run invoke livereload
```

Both serve the site at http://localhost:8000.

## Content

Articles live in `content/articles/`, pages in `content/pages/`, images in `content/images/`.

Files are written in Markdown. Use the `new` task to create a pre-filled file:

```bash
# New article (Status: draft, path relative to content/ or with content/ prefix)
uv run invoke new articles/IT/my-post.md

# New page (detected automatically from path prefix, or via flag)
uv run invoke new pages/my-page.md
uv run invoke new --page articles/my-page.md
```

The title, date, author, and slug are pre-filled from the filename and `pelicanconf.py`.
Set `Status: published` when the article is ready to go live.

## Spell-checking

Check markdown files for spelling errors using hunspell:

```bash
# Check all files (German by default)
uv run invoke spellcheck

# Check a single file or directory
uv run invoke spellcheck --path articles/IT/my-post.md
uv run invoke spellcheck --path articles/IT/

# Check in American English
uv run invoke spellcheck --lang en_US
```

Requires the hunspell dictionaries to be installed:

```bash
sudo pacman -S hunspell-de hunspell-en_us   # Arch / CachyOS
```

To suppress false positives (loanwords, proper nouns, technical terms), add them to
`~/.hunspell_de_DE` (one word per line).

## Deploy

Pushing to `main` triggers a GitHub Actions workflow that builds the site with production
settings and uploads it to the server via rsync.