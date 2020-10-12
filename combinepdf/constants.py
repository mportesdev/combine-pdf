import os

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

TEMP_DIR = os.path.join(HOME_DIR, '.cpdf')

if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)

# Colors

PDF_FILE_BGCOLOR = 0xffd8e8ff
IMG_FILE_BGCOLOR = 0xffd0f0d0
BLANK_PAGE_BGCOLOR = 0xffffffff


# Stylesheets

INVALID = 'color: #000000; background: #ffa0a0;'
INFO_LABEL = 'color: #568dc0'


# Dialog texts

# TODO: make a nicer Help and About dialog
HELP_TEXT = ('In the "Pages" input field, enter single page numbers'
             ' or ranges of page numbers.\n'
             'Example: 1, 3-5, 8\n'
             'will produce page sequence 1, 3, 4, 5, 8\n\n'
             'Order is observed.\n'
             'Example: 2-4, 1\n'
             'will produce page sequence 2, 3, 4, 1\n\n'
             'Repeating is allowed.\n'
             'Example: 1-3, 2, 1-2\n'
             'will produce page sequence 1, 2, 3, 2, 1, 2')

ABOUT_TEXT = ('CombinePDF\n\n'
              'version 0.8.7\n\n'
              '10 November 2019')
