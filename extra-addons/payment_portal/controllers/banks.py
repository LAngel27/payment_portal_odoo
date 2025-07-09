from odoo import http, _
from odoo.http import request
from .portal_payment import PortalPayment

MODEL_PAYMENT_REFERENCE = 'payment.reference.portal.payment'


class PortalPaymentApiBanks(PortalPayment):

    @http.route('/api/portal/banks', type='json', auth='user', csrf=False)
    def bank_accounts(self, **kwargs):
        """
        Returns the list of available bank journals for the selected company.

        Only journals marked as `show_payment_portal = True` will be included.

        Returns:
        ---------
        A list of dictionaries with:
        - id: (int) Journal ID
        - bank_name: (str) Bank or journal name
        - short_code: (str) Internal journal code
        - currency_id: (int) ID of the journal's currency
        - currency_symbol: (str) Currency symbol (e.g. $, Bs)
        - default_account: (int) Default account ID linked to the journal
        """
        journals = request.env['account.journal'].sudo().search([
            ('type', '=', 'bank'),
            ('company_id', '=', request.session.get('selected_company_id')),
            ('show_payment_portal', '=', True),
        ])

        result = [{
            'id': j.id,
            'bank_name': j.name,
            'short_code': j.code,
            'currency_id': j.currency_id.id,
            'currency_symbol': j.currency_id.symbol,
            'default_account': j.default_account_id.id,
        } for j in journals]

        return result