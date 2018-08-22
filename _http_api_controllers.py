"""PytSite Auth UI HTTP API Controllers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime as _datetime
from pytsite import routing as _routing, html as _html, lang as _lang, router as _router, formatters as _formatters
from plugins import auth as _auth, permissions as _permissions, query as _query


class GetBrowserRows(_routing.Controller):
    @staticmethod
    def _get_role_row(role: _auth.AbstractRole) -> dict:

        perms = []
        for perm_name in role.permissions:
            # If permission was renamed or deleted (sometimes it happens), juts ignore it
            if not _permissions.is_permission_defined(perm_name):
                continue

            perm = _permissions.get_permission(perm_name)
            css = 'label label-default permission-' + perm[0]
            if perm[0] == 'admin':
                css += ' label-danger'
            perms.append(str(_html.Span(_lang.t(perm[1]), css=css)))

        role_desc = role.description
        try:
            role_desc = _lang.t(role_desc)
        except _lang.error.Error:
            pass

        m_url = _router.rule_url('auth_admin@form_role_modify',
                                 {'uid': role.uid, '__redirect': _router.rule_url('auth_admin@browse_roles')})
        actions = '<a href="{}" class="btn btn-default btn-light btn-sm">' \
                  '<i class="fa fas fa-edit"></i></a>'.format(m_url)
        d_url = _router.rule_url('auth_admin@form_role_delete',
                                 {'eids': role.uid, '__redirect': _router.rule_url('auth_admin@browse_roles')})
        if role.name not in ('dev', 'admin', 'user', 'anonymous'):
            actions += '&nbsp;<a href="{}" class="btn btn-danger btn-sm">' \
                       '<i class="fa fas fa-remove fa-times"></i></a>'.format(d_url)

        return {
            'name': role.name,
            'description': role_desc,
            'permissions': ' '.join(perms),
            'actions': actions,
        }

    @staticmethod
    def _get_user_row(user: _auth.AbstractUser) -> dict:
        yes = _lang.t('auth_admin@word_yes')

        roles = ''
        for role in sorted(user.roles, key=lambda rl: rl.name):
            css = 'label label-default'
            if role.name in ('admin', 'dev'):
                css += ' label-danger'
            role_desc = role.description
            try:
                role_desc = _lang.t(role_desc)
            except _lang.error.Error:
                pass
            roles += str(_html.Span(role_desc, css=css)) + ' '

        status = user.status
        if status == _auth.USER_STATUS_ACTIVE:
            status_css = 'info'
        elif status == _auth.USER_STATUS_WAITING:
            status_css = 'warning'
        else:
            status_css = 'default'
        status_word = _lang.t('auth@status_' + user.status)
        status = '<span class="label label-{}">{}</span>'.format(status_css, status_word)

        is_online = '<span class="label label-success">{}</span>'.format(yes) \
            if (_datetime.now() - user.last_activity).seconds < 180 else ''

        m_url = _router.rule_url('auth_admin@form_user_modify',
                                 {'uid': user.uid, '__redirect': _router.rule_url('auth_admin@browse_users')})
        actions = '<a href="{}" class="btn btn-default btn-light btn-sm">' \
                  '<i class="fa fas fa-edit"></i></a>'.format(m_url)
        if user != _auth.get_current_user():
            d_url = _router.rule_url('auth_admin@form_user_delete',
                                     {'eids': user.uid, '__redirect': _router.rule_url('auth_admin@browse_users')})
            actions += '&nbsp;<a href="{}" class="btn btn-danger btn-sm">' \
                       '<i class="fa fas fa-remove fa-times"></i></a>'.format(d_url)

        return {
            'login': user.login,
            'first_last_name': user.first_last_name,
            'roles': roles,
            'status': status,
            'is_public': '<span class="label label-info">{}</span>'.format(yes) if user.is_public else '',
            'is_online': is_online,
            'created': _lang.pretty_date_time(user.created),
            'last_activity': _lang.pretty_date_time(user.last_activity),
            'actions': actions,
        }

    def __init__(self):
        super().__init__()

        self.args.add_formatter('limit', _formatters.PositiveInt())
        self.args.add_formatter('offset', _formatters.PositiveInt())

    def exec(self) -> dict:
        if not _auth.get_current_user().is_admin:
            raise self.forbidden()

        e_type = self.arg('e_type')
        sort_order = -1 if self.arg('order') == 'desc' else 1

        query = None
        total = 0
        limit = self.arg('limit', 10)
        skip = self.arg('offset', 0)
        rows = []

        if self.arg('search'):
            query = _query.Query(_query.Text(self.arg('search'), _lang.get_current()))

        if e_type == 'role':
            total = _auth.count_roles() - 2  # Minus admin and dev

            f = _auth.find_roles(query, sort=[(self.arg('sort', 'name'), sort_order)], limit=limit, skip=skip)
            for role in f:
                if role.name in ('admin', 'dev'):
                    continue

                rows.append(self._get_role_row(role))

        elif e_type == 'user':
            total = _auth.count_users()

            for user in _auth.find_users(query, sort=[(self.arg('sort', 'login'), sort_order)], limit=limit, skip=skip):
                rows.append(self._get_user_row(user))

        return {
            'rows': rows,
            'total': total,
        }
