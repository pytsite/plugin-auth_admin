"""Auth Settings Plugin Controllers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import routing as _routing, tpl as _tpl, metatag as _metatag, lang as _lang, util as _util
from plugins import auth as _auth, auth_ui as _auth_ui, admin as _admin
from . import _frm


class Browser(_routing.Controller):
    """Browse Auth Entities
    """

    def exec(self):
        if not _auth.get_current_user().is_admin:
            raise self.forbidden()

        e_type = self.arg('e_type')
        if e_type == 'role':
            _metatag.t_set('title', _lang.t('auth_admin@roles'))
            form = _frm.BrowseRoles(self.request)
        elif e_type == 'user':
            _metatag.t_set('title', _lang.t('auth_admin@users'))
            form = _frm.BrowseUsers(self.request)
        else:
            raise self.server_error('Unknown auth entity type')

        return _admin.render(_tpl.render('auth_admin@form', {'form': form}))


class ModifyForm(_routing.Controller):
    """Create/Modify Auth Entity
    """

    def exec(self):
        if not _auth.get_current_user().is_admin:
            raise self.forbidden()

        e_type = self.arg('e_type')
        uid = self.arg('uid')
        if e_type == 'role':
            _metatag.t_set('title', _lang.t('auth_admin@' + ('create_role' if uid == '0' else 'modify_role')))
            form = _auth_ui.role_form(self.request, role_uid=uid)
        elif e_type == 'user':
            _metatag.t_set('title', _lang.t('auth_admin@' + ('create_user' if uid == '0' else 'modify_user')))
            form = _auth_ui.user_form(self.request, user_uid=uid)
        else:
            raise self.server_error('Unknown entity type')

        return _admin.render(_tpl.render('auth_admin@form', {'form': form}))


class DeleteForm(_routing.Controller):
    """Delete Auth Entities
    """
    def exec(self):
        if not _auth.get_current_user().is_admin:
            raise self.forbidden()

        eids = self.arg('eids')
        if isinstance(eids, str):
            eids = _util.cleanup_list(eids.split(','))

        form = _frm.DeleteEntities(self.request, e_type=self.arg('e_type'), eids=eids)
        form.hide_title = True
        _metatag.t_set('title', form.title)

        return _admin.render(_tpl.render('auth_admin@form', {'form': form}))
