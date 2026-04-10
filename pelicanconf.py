AUTHOR = 'klasch'
SITENAME = 'Die Seiten eines Schneebrenners'
SITEURL = ""

PATH = "content"

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'de'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Atom-Feed", "/feeds/all.atom.xml"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 10

PAGE_ORDER_BY = "sortorder"

MENUITEMS = (
    ("Home", "/"),
    ("IT", "/category/it.html"),
    ("Bildung", "/category/bildung.html"),
    ("Energie", "/category/energie.html"),
    ("Freizeit", "/category/freizeit.html"),
)

DISPLAY_CATEGORIES_ON_MENU = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True