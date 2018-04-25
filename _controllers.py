"""Auth Settings Plugin Controllers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import routing as _routing, tpl as _tpl, metatag as _metatag, lang as _lang
from plugins import auth as _auth, auth_ui as _auth_ui, admin as _admin
from . import _frm


class AdminBrowse(_routing.Controller):
    """Browse Roles or Users
    """

    def exec(self):
        if not _auth.get_current_user().is_admin:
            raise self.forbidden()

        e_type = self.arg('e_type')
        if e_type == 'role':
            _metatag.t_set('title', _lang.t('auth_admin@roles'))
            form = _frm.RolesBrowser()
        elif e_type == 'user':
            _metatag.t_set('title', _lang.t('auth_admin@users'))
            form = _frm.UsersBrowser()
        else:
            raise self.server_error('Unknown entity type')

        return _admin.render(_tpl.render('auth_admin@form', {'form': form}))


class AdminForm(_routing.Controller):
    """Create/Modify User or Role
    """

    def exec(self):
        if not _auth.get_current_user().is_admin:
            raise self.forbidden()

        e_type = self.arg('e_type')
        uid = self.arg('uid')
        if e_type == 'role':
            _metatag.t_set('title', _lang.t('auth_admin@' + ('create_role' if uid == '0' else 'modify_role')))
            form = _auth_ui.form.Role(role_uid=uid)
        elif e_type == 'user':
            _metatag.t_set('title', _lang.t('auth_admin@' + ('create_user' if uid == '0' else 'modify_user')))
            form = _auth_ui.form.User(user_uid=uid)
        else:
            raise self.server_error('Unknown entity type')

        return _admin.render(_tpl.render('auth_admin@form', {'form': form}))
