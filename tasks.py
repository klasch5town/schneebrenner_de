import os
import shlex
import shutil
import sys
import datetime

from invoke import task
from invoke.main import program
from invoke.util import cd
from pelican import main as pelican_main
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

OPEN_BROWSER_ON_SERVE = True
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE_BASE = os.path.join(PROJECT_ROOT, "pelicanconf.py")
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)

CONFIG = {
    "settings_base": SETTINGS_FILE_BASE,
    "settings_publish": os.path.join(PROJECT_ROOT, "publishconf.py"),
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    "deploy_path": SETTINGS["OUTPUT_PATH"],
    # Remote server configuration
    "ssh_user": "websezrvz_3hx63t",
    "ssh_host": "schneebrenner.de",
    "ssh_port": "2244",
    "ssh_path": "/home/websezrvz/html/schneebrenner_de",
    # Host and port for `serve`
    "host": "localhost",
    "port": 8000,
}


@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG["deploy_path"]):
        shutil.rmtree(CONFIG["deploy_path"])
        os.makedirs(CONFIG["deploy_path"])


@task
def build(c):
    """Build local version of site"""
    pelican_run("-s {settings_base}".format(**CONFIG))


@task
def rebuild(c):
    """`build` with the delete switch"""
    pelican_run("-d -s {settings_base}".format(**CONFIG))


@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    pelican_run("-r -s {settings_base}".format(**CONFIG))


@task
def serve(c):
    """Serve site at http://$HOST:$PORT/ (default is localhost:8000)"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG["deploy_path"],
        (CONFIG["host"], CONFIG["port"]),
        ComplexHTTPRequestHandler,
    )

    if OPEN_BROWSER_ON_SERVE:
        # Open site in default browser
        import webbrowser

        webbrowser.open("http://{host}:{port}".format(**CONFIG))

    sys.stderr.write("Serving at {host}:{port} ...\n".format(**CONFIG))
    server.serve_forever()


@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)


@task
def preview(c):
    """Build production version of site"""
    pelican_run("-s {settings_publish}".format(**CONFIG))

@task
def livereload(c):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server

    def cached_build():
        cmd = "-s {settings_base} -e CACHE_CONTENT=true LOAD_CONTENT_CACHE=true"
        pelican_run(cmd.format(**CONFIG))

    cached_build()
    server = Server()
    theme_path = SETTINGS["THEME"]
    watched_globs = [
        CONFIG["settings_base"],
        f"{theme_path}/templates/**/*.html",
    ]

    content_file_extensions = [".md", ".rst"]
    for extension in content_file_extensions:
        content_glob = "{}/**/*{}".format(SETTINGS["PATH"], extension)
        watched_globs.append(content_glob)

    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file_glob = f"{theme_path}/static/**/*{extension}"
        watched_globs.append(static_file_glob)

    for glob in watched_globs:
        server.watch(glob, cached_build)

    if OPEN_BROWSER_ON_SERVE:
        # Open site in default browser
        import webbrowser

        webbrowser.open("http://{host}:{port}".format(**CONFIG))

    server.serve(host=CONFIG["host"], port=CONFIG["port"], root=CONFIG["deploy_path"])


@task
def publish(c):
    """Publish to production via rsync"""
    pelican_run("-s {settings_publish}".format(**CONFIG))
    c.run(
        'rsync --delete --exclude ".DS_Store" -pthrvz -c '
        '-e "ssh -p {ssh_port}" '
        "{} {ssh_user}@{ssh_host}:{ssh_path}".format(
            CONFIG["deploy_path"].rstrip("/") + "/", **CONFIG
        )
    )


@task(help={
    "path": "Path of the new file relative to content/ (e.g. articles/IT/my-post.md or pages/my-page.md)",
    "page": "Create a page instead of an article (auto-detected from path when it starts with pages/)",
})
def new(c, path, page=False):
    """Create a new article or page pre-filled with metadata"""
    from jinja2 import Environment, FileSystemLoader

    content_dir = SETTINGS["PATH"]
    # Accept both "articles/IT/foo.md" and "content/articles/IT/foo.md"
    if path.startswith(content_dir.rstrip("/") + "/") or path.startswith(content_dir.rstrip("/") + os.sep):
        rel_path = os.path.relpath(path, content_dir)
    else:
        rel_path = path
    full_path = os.path.join(content_dir, rel_path)

    if os.path.exists(full_path):
        sys.exit(f"File already exists: {full_path}")

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    is_page = page or rel_path.startswith("pages/")
    template_name = "page.md" if is_page else "article.md"

    stem = os.path.splitext(os.path.basename(rel_path))[0]

    import re
    # Split CamelCase into words, then also replace dashes/underscores
    spaced = re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", stem)
    title = spaced.replace("-", " ").replace("_", " ").title()

    context = {
        "title": title,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "slug": stem,
        "author": LOCAL_SETTINGS.get("AUTHOR", "klasch"),
    }

    templates_dir = os.path.join(PROJECT_ROOT, "templates", "new")
    env = Environment(loader=FileSystemLoader(templates_dir), keep_trailing_newline=True)
    content = env.get_template(template_name).render(context)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created: {full_path}")


@task(help={
    "lang": "Language: 'de' for German (default) or 'en_US' for American English",
    "path": "File or directory to check, relative to content/ (default: all markdown files)",
})
def spellcheck(c, lang="de", path=None):
    """Spell-check markdown content files using hunspell"""
    import re
    import subprocess
    from markdown import markdown

    lang_map = {"de": "de_DE", "de_DE": "de_DE", "en": "en_US", "en_US": "en_US"}
    dict_name = lang_map.get(lang, lang)

    # Verify the dictionary is available
    probe = subprocess.run(
        ["hunspell", "-d", dict_name, "-l"],
        input="test", capture_output=True, text=True,
    )
    if probe.returncode != 0:
        sys.exit(
            f"Dictionary '{dict_name}' not found. "
            f"Install it with: sudo pacman -S hunspell-{lang.lower().replace('_', '_')}"
        )

    content_dir = SETTINGS["PATH"]
    if path:
        if path.startswith(content_dir.rstrip("/") + "/"):
            search_root = path
        else:
            search_root = os.path.join(content_dir, path)
    else:
        search_root = content_dir

    md_files = []
    if os.path.isfile(search_root):
        if search_root.endswith(".md"):
            md_files = [search_root]
    else:
        for root, _, files in os.walk(search_root):
            for f in sorted(files):
                if f.endswith(".md"):
                    md_files.append(os.path.join(root, f))

    if not md_files:
        sys.exit(f"No markdown files found under: {search_root}")

    # Regex matching a Pelican metadata line (e.g. "Title: Foo" or "Tags: a, b")
    meta_line = re.compile(r"^\w[\w\s-]*:.*")

    errors_found = False
    for filepath in md_files:
        with open(filepath, encoding="utf-8") as f:
            lines = f.read().splitlines()

        # Strip leading frontmatter block
        i = 0
        while i < len(lines) and (meta_line.match(lines[i]) or lines[i].strip() == ""):
            i += 1
        body = "\n".join(lines[i:])

        # Markdown → HTML → plain text
        html = markdown(body, extensions=["tables"])
        text = re.sub(r"<[^>]+>", " ", html)
        # Decode HTML entities (e.g. &amp; → &) before further stripping
        import html as html_module
        text = html_module.unescape(text)
        text = re.sub(r"[^\w\s\-äöüÄÖÜß]", " ", text)  # keep word chars + umlauts

        proc = subprocess.run(
            ["hunspell", "-d", dict_name, "-l"],
            input=text, capture_output=True, text=True,
        )
        misspelled = sorted({
            w.strip() for w in proc.stdout.splitlines()
            if w.strip() and not w.strip().startswith("-")
        })

        if misspelled:
            errors_found = True
            rel = os.path.relpath(filepath, content_dir)
            print(f"\n{rel}:")
            for word in misspelled:
                print(f"  {word}")

    if not errors_found:
        print("No spelling errors found.")


def pelican_run(cmd):
    cmd += " " + program.core.remainder  # allows to pass-through args to pelican
    pelican_main(shlex.split(cmd))