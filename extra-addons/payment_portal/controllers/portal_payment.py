from odoo import http, _
from odoo.http import request
from werkzeug.exceptions import NotFound


MODEL_PAYMENT_REFERENCE = 'payment.reference.portal.payment'


class PortalPayment(http.Controller):

    @http.route('/portal/payment', type='http', auth='user', website=True)
    def portal_payment(self, **kwargs):
        """
        Render the main portal payment page if the portal is enabled.

        Route:
        -------
        GET /portal/payment

        Returns:
        ---------
        Renders the payment portal template or raises 404 if disabled.
        """
        enable = request.env['ir.config_parameter'].sudo().get_param('payment_portal.enable_payment_portal')
        if not enable:
            raise NotFound()

        return request.render('payment_portal.portal_payment', {})

    @http.route(['/portal/payment/companies'], type='http', auth="user", website=True, methods=['GET', 'POST'])
    def portal_payment_selected_company(self, **kwargs):
        """
        Allows portal users to select the company context.

        GET:
            Displays a list of companies the user belongs to.
        POST:
            Sets the selected company in the session and redirects to the portal.

        Route:
        -------
        /portal/payment/companies

        Returns:
        ---------
        - On GET: Renders the company selection view.
        - On POST: Sets selected company and redirects to payment portal.
        """
        enable = request.env['ir.config_parameter'].sudo().get_param('payment_portal.enable_payment_portal')
        if not enable:
            raise NotFound()

        if request.httprequest.method == 'POST':
            company_id = int(kwargs.get('company_id', 0))
            request.session['selected_company_id'] = company_id
            return request.redirect('/portal/payment')
        else:
            companies = request.env.user.company_ids
            return request.render("payment_portal.portal_selected_company", {
                'companies': companies
            })