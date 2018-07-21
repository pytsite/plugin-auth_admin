"""PytSite Auth Admin Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import html as _html, router as _router
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

        super().__init__(uid, rows_url=rows_url, data_fields=data_fields, checkbox=False, **kwargs)

        add_btn_url = _router.rule_url('auth_admin@form_role_modify',
                                       {'uid': '0', '__redirect': _router.rule_url('auth_admin@browse_roles')})
        add_btn = _html.A(href=add_btn_url, css='btn btn-default btn-light')
        add_btn.append(_html.I(css='fa fa-plus'))
        self.toolbar.append(add_btn)


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

        super().__init__(uid, rows_url=rows_url, data_fields=data_fields, checkbox=False, **kwargs)

        add_btn_url = _router.rule_url('auth_admin@form_user_modify',
                                       {'uid': '0', '__redirect': _router.rule_url('auth_admin@browse_users')})
        add_btn = _html.A(href=add_btn_url, css='btn btn-default btn-light')
        add_btn.append(_html.I(css='fa fa-plus'))
        self.toolbar.append(add_btn)
