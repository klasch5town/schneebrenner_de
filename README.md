Schneebrenner Homepage Repository
=================================

This is a repository hosting the source for my homepage at https://www.schneebrenner.de.

I started to create my homepage with the help of the static site generator [pelican](https://getpelican.com/) in order
to get rid of Wordpress as this is immoderate for a small private homepage.
As building the statice site with Pelican process also includes a build-step (like in software development)
and as I'm used to repositories as an software developer I decided to store the 'homepage sources' at github.

Further advantages are that I can track the changes and have it stored not just at my server and local computer (a kind of backup).

And last but not least I use this repository to get into the stuff of automated builds with help of [buildbot](https://www.buildbot.net/). I'm used to Jenkins but wanted to try out buildbot for such a long time. But this is another story worth to be documented in another repository - the homepage buildbot repository.

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

Articles live in `content/articels/`, pages in `content/pages/`, images in `content/images/`.

Files are written in Markdown. A new article looks like this:

```markdown
Title: My article title
Date: 2026-04-10
Category: Linux

Content goes here.
```

## Deploy

Pushing to `main` triggers a GitHub Actions workflow that builds the site with production
settings and uploads it to the server via rsync. See `doc/planning.md` for the one-time
SSH key setup required to make that work.