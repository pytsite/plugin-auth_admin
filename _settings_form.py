"""PytSite Authentication Settings Plugin Forms
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang as _lang
from plugins import widget as _widget, auth_ui as _auth_ui, settings as _settings, auth as _auth


class Form(_settings.Form):
    """PytSite Auth Settings Form
    """

    def _on_setup_widgets(self):
        self.add_widget(_widget.select.Checkbox(
            weight=10,
            uid='setting_signup_enabled',
            label=_lang.t('auth_settings@allow_sign_up'),
            default=_auth.is_sign_up_enabled(),
        ))

        self.add_widget(_widget.select.Checkbox(
            weight=20,
            uid='setting_signup_confirmation_required',
            label=_lang.t('auth_settings@signup_confirmation_required'),
            default=_auth.is_sign_up_confirmation_required(),
        ))

        self.add_widget(_widget.select.Checkbox(
            weight=30,
            uid='setting_signup_admins_notification_enabled',
            label=_lang.t('auth_settings@signup_notify_admins'),
            default=_auth.is_sign_up_admins_notification_enabled(),
        ))

        ui_driver_items = [(driver.name, driver.description) for driver in _auth_ui.get_drivers().values()]
        self.add_widget(_widget.select.Select(
            weight=40,
            uid='setting_ui_driver',
            append_none_item=False,
            label=_lang.t('auth_settings@default_ui_driver'),
            h_size='col-xs-12 col-sm-6 col-md-3',
            items=sorted(ui_driver_items, key=lambda i: i[0]),
            default=_auth_ui.get_driver().name,
        ))

        self.add_widget(_widget.select.Select(
            weight=50,
            uid='setting_new_user_status',
            append_none_item=False,
            label=_lang.t('auth_settings@new_user_status'),
            h_size='col-xs-12 col-sm-6 col-md-3',
            items=_auth.get_user_statuses(),
            default=_auth.get_new_user_status(),
        ))

        self.add_widget(_widget.select.Checkboxes(
            weight=60,
            uid='setting_new_user_roles',
            label=_lang.t('auth_settings@new_user_roles'),
            h_size='col-xs-12 col-sm-6 col-md-3',
            items=[(r.name, _lang.t(r.description)) for r in _auth.find_roles()],
            default=['user'],
        ))

        super()._on_setup_widgets()
