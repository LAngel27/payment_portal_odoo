from odoo import http, _
from odoo.http import request
from datetime import date
from .portal_payment import PortalPayment

MODEL_PAYMENT_REFERENCE = 'payment.reference.portal.payment'

class PortalPaymentApiInvoices(PortalPayment):
    
    @http.route('/api/portal/invoices', type='json', auth="user", csrf=False)
    def invoice_end_point(self, **kwargs):
        """
        Fetches a list of invoices associated with the logged-in portal user.

        Parameters (via JSON payload):
        --------------------------------
        - date: (str) Exact invoice date in YYYY-MM-DD format
        - payment_state: (str) Payment status ('paid', 'not_paid', etc.)
        - name: (str) Partial search for invoice number
        - expired_invoice: (bool) If True, only fetch overdue invoices
        - current_invoice: (bool) If True, only fetch current or upcoming invoices
        - offset: (int) Pagination offset (default: 0)
        - limit: (int) Max number of results (default: 50, max: 100)

        Returns:
        ---------
        A list of dictionaries with key invoice information.
        """
        user = request.env.user
        company_id = request.session.get('selected_company_id') or request.env.company.id
        domain = [
            ('move_type', 'in', ['out_invoice', 'out_refund', 'out_debit', 'out_note']),
            ('partner_id', '=', user.commercial_partner_id.id),
            ('company_id', '=', company_id)
        ]
        
        kwargs = kwargs['params']

        if kwargs.get('date'):
            domain.append(('invoice_date', '=', kwargs['date']))
        if kwargs.get('payment_state') and kwargs['payment_state'] not in ['defeated', 'current']:
            domain.append(('payment_state', '=', kwargs['payment_state']))
        if kwargs.get('name'):
            domain += [('name', 'ilike', kwargs['name'])]
        if kwargs.get('expired_invoice'):
            domain.append(('invoice_date_due', '<', date.today()))
        if kwargs.get('current_invoice'):
            domain.append(('invoice_date_due', '>=', date.today()))

        offset = int(kwargs.get('offset') or 0)
        limit = min(int(kwargs.get('limit', 50)), 100)

        invoices = request.env['account.move'].sudo().search(domain, limit=limit, offset=offset, order='invoice_date desc')
        invoices = [{
            'id': inv.id,
            'number': inv.name,
            'date': inv.invoice_date.strftime('%d/%m/%Y') if inv.invoice_date else '',
            'total': inv.amount_total_signed,
            'type_currency': inv.currency_id.id,
            'state': inv.payment_state,
            'amount_residual': inv.amount_residual,
            'date_due': inv.invoice_date_due,
            'due_for_pay': inv.invoice_date_due < date.today() if inv.invoice_date_due else False,
        } for inv in invoices]
        
        return invoices