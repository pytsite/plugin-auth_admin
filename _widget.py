"""PytSite Auth Admin Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from pytsite import router
from plugins import widget, http_api


class RolesBrowser(widget.misc.BootstrapTable):
    def __init__(self, uid: str, **kwargs):
        rows_url = http_api.url('auth_admin@browser_rows', {'e_type': 'role'})

        data_fields = [
            ('name', 'auth_admin@name', True),
            ('description', 'auth_admin@description', False),
            ('permissions', 'auth_admin@permissions', False),
            ('_actions', 'auth_admin@actions', False),
        ]

        super().__init__(uid, rows_url=rows_url, data_fields=data_fields, checkbox=False, **kwargs)

        add_btn_url = router.rule_url('auth_admin@form_role_modify',
                                      {'uid': '0', '__redirect': router.rule_url('auth_admin@browse_roles')})
        add_btn = htmler.A(href=add_btn_url, css='btn btn-default btn-light')
        add_btn.append_child(htmler.I(css='fa fa-plus'))
        self.toolbar.append_child(add_btn)

        self._css += ' widget-auth-admin-browser'


class UsersBrowser(widget.misc.BootstrapTable):
    def __init__(self, uid: str, **kwargs):
        rows_url = http_api.url('auth_admin@browser_rows', {'e_type': 'user'})

        data_fields = [
            ('login', 'auth_admin@login', True),
            ('first_last_name', 'auth_admin@full_name', True),
            ('roles', 'auth_admin@roles', False),
            ('status', 'auth_admin@status', True),
            ('is_public', 'auth_admin@is_public', True),
            ('is_online', 'auth_admin@is_online', True),
            ('created', 'auth_admin@created', True),
            ('last_activity', 'auth_admin@last_activity', True),
            ('_actions', 'auth_admin@actions', False),
        ]

        super().__init__(uid, rows_url=rows_url, data_fields=data_fields, checkbox=False, **kwargs)

        add_btn_url = router.rule_url('auth_admin@form_user_modify',
                                      {'uid': '0', '__redirect': router.rule_url('auth_admin@browse_users')})
        add_btn = htmler.A(href=add_btn_url, css='btn btn-default btn-light')
        add_btn.append_child(htmler.I(css='fa fa-plus'))
        self.toolbar.append_child(add_btn)

        self._css += ' widget-auth-admin-browser'
