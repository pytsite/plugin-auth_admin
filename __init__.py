"""PytSite Auth Settings Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load_uwsgi():
    from pytsite import lang, router, tpl
    from plugins import settings, admin, http_api
    from . import _frm, _controllers, _http_api_controllers

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)

    # Settings form
    settings.define('auth', _frm.Settings, 'auth_admin@security', 'fa fa-user', 'dev')

    # BAse path for route rules
    abp = admin.base_path() + '/auth'

    # HTTP API rules
    http_api.handle('GET', abp + '/browse/<e_type>', _http_api_controllers.GetBrowserRows, 'auth_admin@browser_rows')

    # Admin routes
    router.handle(_controllers.AdminBrowse, abp + '/role', 'auth_admin@browse_roles', {'e_type': 'role'})
    router.handle(_controllers.AdminBrowse, abp + '/user', 'auth_admin@browse_users', {'e_type': 'user'})
    router.handle(_controllers.AdminForm, abp + '/role/<uid>', 'auth_admin@form_role', {'e_type': 'role'})
    router.handle(_controllers.AdminForm, abp + '/user/<uid>', 'auth_admin@form_user', {'e_type': 'user'})

    # 'Security' admin sidebar section
    admin.sidebar.add_section('security', 'auth_admin@security', 1000)

    # 'Users' admin sidebar menu
    path = router.rule_path('auth_admin@browse_users')
    admin.sidebar.add_menu('security', 'users', 'auth_admin@users', path, 'fa fa-users', weight=10)

    # 'Roles' admin sidebar menu
    path = router.rule_path('auth_admin@browse_roles')
    admin.sidebar.add_menu('security', 'roles', 'auth_admin@roles', path, 'fa fa-key', weight=20, roles='dev')
