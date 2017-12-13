"""PytSite Auth Settings Plugin
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load():
    from pytsite import lang
    from plugins import settings
    from . import _settings_form

    # Localization resources
    lang.register_package(__name__)

    # Settings form
    settings.define('auth', _settings_form.Form, 'auth_settings@security', 'fa fa-user')
