"""PytSite Authentication Settings Plugin Forms
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang as _lang, html as _html, errors as _errors, router as _router
from plugins import widget as _widget, auth_ui as _auth_ui, settings as _settings, auth as _auth, form as _form
from . import _widget as _w


class Settings(_settings.Form):
    """PytSite Auth Settings Form
    """

    def _on_setup_widgets(self):
        self.add_widget(_widget.select.Checkbox(
            uid='setting_signup_enabled',
            label=_lang.t('auth_admin@allow_sign_up'),
            default=_auth.is_sign_up_enabled(),
        ))

        self.add_widget(_widget.select.Checkbox(
            uid='setting_signup_confirmation_required',
            label=_lang.t('auth_admin@signup_confirmation_required'),
            default=_auth.is_sign_up_confirmation_required(),
        ))

        self.add_widget(_widget.select.Checkbox(
            uid='setting_signup_admins_notification_enabled',
            label=_lang.t('auth_admin@signup_notify_admins'),
            default=_auth.is_sign_up_admins_notification_enabled(),
        ))

        self.add_widget(_widget.select.Checkbox(
            uid='setting_user_status_change_notification_enabled',
            label=_lang.t('auth_admin@user_status_change_notify'),
            default=_auth.is_user_status_change_notification_enabled(),
        ))

        ui_driver_items = [(driver.name, driver.description) for driver in _auth_ui.get_drivers().values()]
        self.add_widget(_widget.select.Select(
            uid='setting_ui_driver',
            append_none_item=False,
            label=_lang.t('auth_admin@default_ui_driver'),
            h_size='col-xs-12 col-sm-6 col-md-3',
            items=sorted(ui_driver_items, key=lambda i: i[0]),
            default=_auth_ui.get_driver().name,
        ))

        self.add_widget(_widget.select.Select(
            uid='setting_new_user_status',
            append_none_item=False,
            label=_lang.t('auth_admin@new_user_status'),
            h_size='col-xs-12 col-sm-6 col-md-3',
            items=_auth.get_user_statuses(),
            default=_auth.get_new_user_status(),
        ))

        skip_roles = ['dev', 'admin', 'anonymous']
        self.add_widget(_widget.select.Checkboxes(
            uid='setting_new_user_roles',
            label=_lang.t('auth_admin@new_user_roles'),
            h_size='col-xs-12 col-sm-6 col-md-3',
            items=[(r.name, _lang.t(r.description)) for r in _auth.find_roles() if r.name not in skip_roles],
            default=['user'],
        ))

        super()._on_setup_widgets()


class BrowseRoles(_form.Form):
    def _on_setup_form(self):
        self.submit_button = None

    def _on_setup_widgets(self):
        self.add_widget(_w.RolesBrowser(
            uid='roles_browser',
        ))


class BrowseUsers(_form.Form):
    def _on_setup_form(self):
        self.submit_button = None

    def _on_setup_widgets(self):
        self.add_widget(_w.UsersBrowser(
            uid='users_browser',
        ))


class DeleteEntities(_form.Form):
    def _on_setup_form(self):
        if self.attr('e_type') not in ('role', 'user'):
            raise ValueError('Auth entity type is not specified')

        if not self.attr('eids'):
            raise ValueError('Entity IDs is not specified')

        if self.attr('e_type') == 'role':
            self.title = _lang.t('auth_admin@delete_roles')
        else:
            self.title = _lang.t('auth_admin@delete_users')

        _lang.t('auth_admin@delete_roles')

    def _on_setup_widgets(self):
        e_type = self.attr('e_type')
        eids = self.attr('eids', [])
        ol = _html.Ol()
        for eid in eids:
            if e_type == 'role':
                ol.append(_html.Li(_auth.get_role(uid=eid).name))
            elif e_type == 'user':
                ol.append(_html.Li(_auth.get_user(uid=eid).login))

        self.add_widget(_widget.static.Text(
            uid='confirmation_text',
            text=_lang.t('auth_admin@delete_{}_confirmation'.format(self.attr('e_type'))),
        ))

        self.add_widget(_widget.static.HTML(
            uid='uids_text',
            em=ol,
        ))

        self.add_widget(_widget.button.Link(
            uid='action_cancel',
            weight=100,
            form_area='footer',
            href=self.redirect,
            value=_lang.t('auth_admin@cancel'),
            icon='fa fas fa-ban'
        ))

        self.submit_button.color = 'btn btn-danger'
        self.submit_button.icon = 'fa fas fa-trash'
        self.submit_button.value = _lang.t('auth_admin@delete')

    def _on_submit(self):
        e_type = self.attr('e_type')
        eids = self.attr('eids', [])

        try:
            for eid in eids:
                if e_type == 'role':
                    _auth.get_role(uid=eid).delete()
                elif e_type == 'user':
                    _auth.get_user(uid=eid).delete()
        except _errors.ForbidDeletion as e:
            _router.session().add_error_message(str(e))
            return
