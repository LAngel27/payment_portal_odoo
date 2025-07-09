from odoo import http, _
from odoo.http import request
from .portal_payment import PortalPayment


class PortalPaymentApICurrencies(PortalPayment):
    
    @http.route('/api/portal/currencies', type='json', auth='user', csrf=False)
    def active_currencies(self, **kwargs):
        """
        Returns a list of all active currencies available in the system.

        Returns:
        ---------
        A list of dictionaries with:
        - currency_id: (int) Currency ID
        - currency_name: (str) Currency code (e.g. USD, EUR)
        - symbol: (str) Currency symbol (e.g. $, €)
        """
        currencies = request.env['res.currency'].sudo().search([('active', '=', True)])

        currencies = [{
            'currency_id': c.id,
            'currency_name': c.name,
            'symbol': c.symbol,
        } for c in currencies]

        return currencies