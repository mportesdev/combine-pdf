import os

VERSION = '0.9.0'


# Main window

WINDOW_TITLE = 'CombinePDF'
WINDOW_SIZE = (640, 300)


# Paths

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
ICON_DIR = os.path.join(PROJECT_DIR, 'icons')

ICON_COMBINE = os.path.join(ICON_DIR, 'combine.png')
ICON_EXIT = os.path.join(ICON_DIR, 'exit.png')
ICON_QUESTION = os.path.join(ICON_DIR, 'question.png')
ICON_INFO = os.path.join(ICON_DIR, 'info.png')
ICON_TRASH = os.path.join(ICON_DIR, 'trash.png')
ICON_PLUS = os.path.join(ICON_DIR, 'plus.png')

try:
    HOME_DIR = os.environ['HOME']
except KeyError:
    HOME_DIR = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])

# By default, config file and temporary files are stored in $HOME/.cpdf
# This can be overridden by setting an environment variable CPDFLOCALDIR
LOCAL_DIR = os.getenv('CPDFLOCALDIR', os.path.join(HOME_DIR, '.cpdf'))

CONFIG_PATH = os.path.join(LOCAL_DIR, 'config.json')
TEMP_DIR = os.path.join(LOCAL_DIR, 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)


# Colors

PDF_FILE_BGCOLOR = 0xffd8e8ff
IMG_FILE_BGCOLOR = 0xffd0f0d0
BLANK_PAGE_BGCOLOR = 0xffffffff


# Stylesheets

INVALID = 'color: #000000; background: #ffa0a0;'
INFO_LABEL = 'color: #568dc0'


# Dialog texts

HELP_TEXT = """
In the "Pages" input field, enter single page numbers or ranges of page numbers.

Example:
1, 3-5, 8
will produce page sequence 1, 3, 4, 5, 8

Example:
2-4, 1
will produce page sequence 2, 3, 4, 1

Example:
1-3, 2, 1-2
will produce page sequence 1, 2, 3, 2, 1, 2
"""

ABOUT_TEXT = f"""
CombinePDF

version {VERSION}

12 October 2020
"""

NO_OVERWRITE_TEXT = """
You are not allowed to overwrite one of the input files.

Please select a different filename.
"""
