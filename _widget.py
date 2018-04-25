"""PytSite Auth Admin Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins import widget as _widget, http_api as _http_api


class RolesBrowser(_widget.misc.BootstrapTable):
    def __init__(self, uid: str, **kwargs):
        rows_url = _http_api.url('auth_admin@browser_rows', {'e_type': 'role'})

        data_fields = [
            ('name', 'auth_admin@name', True),
            ('description', 'auth_admin@description', False),
            ('permissions', 'auth_admin@permissions', False),
            ('actions', 'auth_admin@actions', False),
        ]

        super().__init__(uid, rows_url=rows_url, data_fields=data_fields, **kwargs)


class UsersBrowser(_widget.misc.BootstrapTable):
    def __init__(self, uid: str, **kwargs):
        rows_url = _http_api.url('auth_admin@browser_rows', {'e_type': 'user'})

        data_fields = [
            ('login', 'auth_admin@login', True),
            ('full_name', 'auth_admin@full_name', True),
            ('roles', 'auth_admin@roles', False),
            ('status', 'auth_admin@status', True),
            ('is_public', 'auth_admin@is_public', True),
            ('is_online', 'auth_admin@is_online', True),
            ('created', 'auth_admin@created', True),
            ('last_activity', 'auth_admin@last_activity', True),
            ('actions', 'auth_admin@actions', False),
        ]

        super().__init__(uid, rows_url=rows_url, data_fields=data_fields, **kwargs)
