#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals


###########################
#  Pelican Version 4.2.0  #
###########################

####################
#  Basic settings  #
####################
USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = 'Misc'
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
DOCUTILS_SETTINGS = {}
DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = []
JINJA_ENVIRONMENT = {
    'trim_blocks': True,
    'lstrip_blocks': True,
}
JINJA_FILTERS = {}
LOG_FILTER = []
READERS = {}
IGNORE_FILES = ['.#*']
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}
OUTPUT_PATH = 'output'
PATH = 'content'
PAGE_PATHS = ['pages']
PAGE_EXCLUDES = []
ARTICLE_PATHS = ['articles']
ARTICLE_EXCLUDES = []
OUTPUT_SOURCES = False
OUTPUT_SOURCES_EXTENSION = '.text'
PLUGINS = []
PLUGIN_PATHS = []
SITENAME = '荒田半亩'
SITEURL = '//note.yycrazy.net/'
STATIC_PATHS = ['uploads', 'extras']
STATIC_EXCLUDES = []
STATIC_EXCLUDE_SOURCES = True
STATIC_CREATE_LINKS = False
STATIC_CHECK_IF_MODIFIED = False
TYPOGRIFY = False
TYPOGRIFY_IGNORE_TAGS = []
SUMMARY_MAX_LENGTH = 50
WITH_FUTURE_DATES = True
INTRASITE_LINK_REGEX = '[{|](?P<what>.*?)[|}]'
PYGMENTS_RST_OPTIONS = []
SLUGIFY_SOURCE = 'title'
CACHE_CONTENT = False
CONTENT_CACHING_LAYER = 'reader'
CACHE_PATH = 'cache'
GZIP_CACHE = True
CHECK_MODIFIED_METHOD = 'mtime'
LOAD_CONTENT_CACHE = False
WRITE_SELECTED = []
FORMATTED_FIELDS = ['summary']
PORT = 8000
BIND = ''

##################
#  URL Settings  #
##################
RELATIVE_URLS = False
ARTICLE_URL = '{slug}.html'
ARTICLE_SAVE_AS = '{slug}.html'
ARTICLE_LANG_URL = '{slug}-{lang}.html'
ARTICLE_LANG_SAVE_AS = '{slug}-{lang}.html'
DRAFT_URL = 'drafts/{slug}.html'
DRAFT_SAVE_AS = 'drafts/{slug}.html'
DRAFT_LANG_URL = 'drafts/{slug}-{lang}.html'
DRAFT_LANG_SAVE_AS = 'drafts/{slug}-{lang}.html'
PAGE_URL = 'pages/{slug}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'
PAGE_LANG_URL = 'pages/{slug}-{lang}.html'
PAGE_LANG_SAVE_AS = 'pages/{slug}-{lang}.html'
DRAFT_PAGE_URL = 'drafts/pages/{slug}.html'
DRAFT_PAGE_SAVE_AS = 'drafts/pages/{slug}.html'
DRAFT_PAGE_LANG_URL = 'drafts/pages/{slug}-{lang}.html'
DRAFT_PAGE_LANG_SAVE_AS = 'drafts/pages/{slug}-{lang}.html'
AUTHOR_URL = ''
AUTHOR_SAVE_AS = ''
CATEGORY_URL = 'categories/{slug}.html'
CATEGORY_SAVE_AS = 'categories/{slug}.html'
TAG_URL = 'tags/{slug}.html'
TAG_SAVE_AS = 'tags/{slug}.html'
YEAR_ARCHIVE_URL = ''
YEAR_ARCHIVE_SAVE_AS = ''
MONTH_ARCHIVE_URL = ''
MONTH_ARCHIVE_SAVE_AS = ''
DAY_ARCHIVE_URL = ''
DAY_ARCHIVE_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORIES_SAVE_AS = 'categories/index.html'
TAGS_SAVE_AS = 'tags/index.html'
INDEX_SAVE_AS = 'index.html'
SLUG_REGEX_SUBSTITUTIONS = [
    (r'[^\w\s-]', ''),  # remove non-alphabetical/whitespace/'-' chars
    (r'(?u)\A\s*', ''), # strip leading whitespace
    (r'(?u)\s*\Z', ''), # strip trailing whitespace
    (r'[-\s]+', '-'),   # reduce multiple whitespace or '-' to single '-'
]
AUTHOR_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS
CATEGORY_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS
TAG_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS

###################
#  Time and Date  #
###################
TIMEZONE = 'Asia/Shanghai'
DEFAULT_DATE = None
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMATS = {}
# LOCALE

####################
#  Template pages  #
####################
TEMPLATE_PAGES = None
TEMPLATE_EXTENSIONS = ['.html']
DIRECT_TEMPLATES = ['index', 'categories', 'tags', 'archives']

##############
#  Metadata  #
##############
AUTHOR = 'YYCrazy'
DEFAULT_METADATA = {}
FILENAME_METADATA = '(?P<date>d{4}-d{2}-d{2}).*'
PATH_METADATA = ''
EXTRA_PATH_METADATA = {}
EXTRA_PATH_METADATA = {
    'extras/robots.txt': {'path': 'robots.txt'},
}

###################
#  Feed Settings  #
###################
FEED_DOMAIN = None
FEED_ATOM = None
FEED_ATOM_URL = None
FEED_RSS = None
FEED_RSS_URL = None
FEED_ALL_ATOM = None
FEED_ALL_ATOM_URL = None
FEED_ALL_RSS = None
FEED_ALL_RSS_URL = None
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_ATOM_URL = None
CATEGORY_FEED_RSS = None
CATEGORY_FEED_RSS_URL = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_ATOM_URL = None
AUTHOR_FEED_RSS = None
AUTHOR_FEED_RSS_URL = None
TAG_FEED_ATOM = None
TAG_FEED_ATOM_URL = None
TAG_FEED_RSS = None
# FEED_MAX_ITEMS
RSS_FEED_SUMMARY_ONLY = True

################
#  Pagination  #
################
DEFAULT_ORPHANS = 0
DEFAULT_PAGINATION = False
PAGINATED_TEMPLATES = {'index': None, 'tag': None, 'category': None, 'author': None}
PAGINATION_PATTERNS = (
    (1, '{name}{extension}', '{name}{extension}'),
    (2, '{name}{number}{extension}', '{name}{number}{extension}'),
)

##################
#  Translations  #
##################
DEFAULT_LANG = 'zh'
ARTICLE_TRANSLATION_ID = 'slug'
PAGE_TRANSLATION_ID = 'slug'
TRANSLATION_FEED_ATOM = None
TRANSLATION_FEED_ATOM_URL = None
TRANSLATION_FEED_RSS = None
TRANSLATION_FEED_RSS_URL = None

######################
#  Ordering content  #
######################
NEWEST_FIRST_ARCHIVES = True
REVERSE_CATEGORY_ORDER = False
ARTICLE_ORDER_BY = 'reversed-date'
PAGE_ORDER_BY = 'basename'

############
#  Themes  #
############
THEME = 'themes/ysimple'
THEME_STATIC_DIR = 'static'
THEME_STATIC_PATHS = ['static']
THEME_TEMPLATES_OVERRIDES = []
MENUITEMS = (
    ('首页', '//note.yycrazy.net/'),
    ('分类', '//note.yycrazy.net/categories/index.html'),
    ('标签', '//note.yycrazy.net/tags/index.html'),
)
