# -*- coding: utf-8 -*-
import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
ENV_LOCALE_DIR = 'PYTHON_VALIDATOR_LOCALE'
ENV_LANGUAGES = 'PYTHON_VALIDATOR_LANGUAGES'
DEFAULT_LOCALE_DIR = os.path.join(BASE_PATH, 'locale')
DOMAIN = 'python-validator'

domain = DOMAIN 
localedir = os.environ.get(ENV_LOCALE_DIR, DEFAULT_LOCALE_DIR)
languages = os.environ.get(ENV_LANGUAGES)
if languages is not None:
    try:
        languages = languages.split(',')
    except:
        languages = None

try:
    # try using Django's translation tool
    from django.utils.translation import gettext, ngettext
except ImportError as e:
    import gettext as _gettext
    translation = _gettext.translation(domain, localedir, languages=languages, fallback=True)

    def get_localedir():
        return localedir

    def gettext(s):
        return translation.gettext(s)

    def ngettext(singular, plural, n):
        return translation.ngettext(singular, plural, n)
    
    def lgettext(s):
        return translation.lgettext(s)
    
    def lngettext(singular, plural, n):
        return translation.lngettext(singular, plural, n)
