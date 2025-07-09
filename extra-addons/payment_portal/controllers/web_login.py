import odoo
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, AccessDenied
from odoo.addons.web.controllers.utils import ensure_db,  is_user_internal
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.session import Session
from werkzeug.exceptions import NotFound


SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                        'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                        'password', 'confirm_password', 'city', 'country_id', 'lang', 'signup_email'}


CREDENTIAL_PARAMS = ['login', 'password', 'type']


class OAuthLoginPortalPayment(Home):

    def _login_redirect(self, uid, redirect=None):
        """
        Custom redirect after successful login for portal users.

        If no redirect is provided and the user is a payment portal user,
        redirect them to the company selection page.

        Parameters:
        -----------
        uid: int
            User ID of the logged-in user.
        redirect: str or None
            Optional custom redirect URL.

        Returns:
        --------
        str: Redirect URL
        """
        if not redirect and not is_user_internal(uid):
            user = request.env.user
            if user and user.is_user_portal_payment:
                redirect = '/portal/payment/companies'
        return super()._login_redirect(uid, redirect=redirect)
    

    @http.route('/login/portal/payment', type='http', auth='none', readonly=False)
    def login_portal_payment(self, redirect=None, **kw):
        """
        Renders the custom login page for portal payment users and handles login POST.

        Supports both GET (login form) and POST (form submission) methods.

        Parameters:
        -----------
        redirect: str or None
            Redirect URL after successful login.
        kw: dict
            Additional parameters passed via form or query string.

        Returns:
        --------
        werkzeug.wrappers.Response
        """
        ensure_db()
        request.params['login_success'] = False

        # Redirect immediately if already logged in
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        # Simulate hybrid auth (auth=user or auth=public)
        if request.env.uid is None:
            if request.session.uid is None:
                request.env["ir.http"]._auth_method_public()
            else:
                request.update_env(user=request.session.uid)

        # Prepare values for rendering
        values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        # Handle login submission
        if request.httprequest.method == 'POST':
            try:
                credential = {
                    key: value for key, value in request.params.items()
                    if key in CREDENTIAL_PARAMS and value
                }
                credential.setdefault('type', 'password')
                auth_info = request.session.authenticate(request.db, credential)
                request.params['login_success'] = True
                return request.redirect(self._login_redirect(auth_info['uid'], redirect=redirect))
            except AccessDenied as e:
                if e.args == AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if request.params.get('error') == 'access':
                values['error'] = _('Only employees can access this database. Please contact the administrator.')

        # Prefill login field if previously used
        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        # Disable DB selector if restricted by config
        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        # Render the login page
        response = request.render('payment_portal.login_portal', values)
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response


class SessionWebsiteInherit(Session):

    @http.route('/web/session/logout', type='http', auth="none", website=True, multilang=False, sitemap=False)
    def logout(self, redirect='/web'):
        """
        Override logout to redirect portal payment users to their login page.

        Parameters:
        -----------
        redirect: str
            URL to redirect after logout.

        Returns:
        --------
        werkzeug.wrappers.Response
        """
        user = request.env.user.sudo().search([
            ('id', '=', request.session._Session__data['context']['uid'])
        ])
        if user.is_user_portal_payment:
            return super().logout(redirect='/login/portal/payment')
        return super().logout(redirect=redirect)