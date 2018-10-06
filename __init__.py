"""PytSite Auth Settings Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load_wsgi():
    from pytsite import router
    from plugins import auth_ui, settings, admin, http_api
    from . import _frm, _controllers, _http_api_controllers

    # Settings form
    settings.define('auth', _frm.Settings, 'auth_admin@security', 'fa fa-user', 'dev')

    # BAse path for route rules
    abp = admin.base_path() + '/auth'

    # HTTP API rules
    http_api.handle('GET', abp + '/browse/<e_type>', _http_api_controllers.GetBrowserRows, 'auth_admin@browser_rows')

    # Admin routes
    flt = auth_ui.AuthFilter
    router.handle(_controllers.Browser, abp + '/browse/role', 'auth_admin@browse_roles',
                  {'e_type': 'role'}, filters=flt)
    router.handle(_controllers.Browser, abp + '/browse/user', 'auth_admin@browse_users',
                  {'e_type': 'user'}, filters=flt)
    router.handle(_controllers.ModifyForm, abp + '/modify/role/<uid>', 'auth_admin@form_role_modify',
                  {'e_type': 'role'}, filters=flt)
    router.handle(_controllers.ModifyForm, abp + '/modify/user/<uid>', 'auth_admin@form_user_modify',
                  {'e_type': 'user'}, filters=flt)
    router.handle(_controllers.DeleteForm, abp + '/delete/role', 'auth_admin@form_role_delete',
                  {'e_type': 'role'}, ('GET', 'POST'), flt)
    router.handle(_controllers.DeleteForm, abp + '/delete/user', 'auth_admin@form_user_delete',
                  {'e_type': 'user'}, ('GET', 'POST'), flt)

    # 'Security' admin sidebar section
    admin.sidebar.add_section('security', 'auth_admin@security', 1000)

    # 'Users' admin sidebar menu
    admin.sidebar.add_menu('security', 'users', 'auth_admin@users', router.rule_path('auth_admin@browse_users'),
                           'fa fa-users', weight=10)

    # 'Roles' admin sidebar menu
    admin.sidebar.add_menu('security', 'roles', 'auth_admin@roles', router.rule_path('auth_admin@browse_roles'),
                           'fa fa-key', weight=20, roles='dev')
