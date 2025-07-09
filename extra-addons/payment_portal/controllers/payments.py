from odoo import http, _
from odoo.http import request
from .portal_payment import PortalPayment
import base64
import logging

_logger = logging.getLogger(__name__)

MODEL_PAYMENT_REFERENCE = 'payment.reference.portal.payment'


class PortalPaymentApiPayments(PortalPayment):
    
    @http.route('/api/portal/payments', type='json', auth="user", csrf=False)
    def payments_end_point(self, **kwargs):
        """
        Retrieve payments registered by the logged-in portal user.

        Parameters (via JSON):
        -----------------------
        - date: (str) Exact payment date (YYYY-MM-DD)
        - state: (str) Payment state ('draft', 'confirmed', etc.)
        - name: (str) Search by payment number
        - offset: (int) Pagination offset
        - limit: (int) Max number of records (default: 50, max: 100)

        Returns:
        ---------
        A list of payment records in dictionary format.
        """
        user = request.env.user
        company_id = request.session.get('selected_company_id') or request.env.company.id

        domain = [
            ('partner_id', '=', user.commercial_partner_id.id),
            ('state', 'in', ['draft', 'confirmed']),
            ('company_id', '=', company_id),
        ]

        kwargs = kwargs.get('params', {})

        if kwargs.get('date'):
            domain.append(('payment_date', '=', kwargs['date']))
        if kwargs.get('state'):
            domain.append(('state', '=', kwargs['state']))
        if kwargs.get('name'):
            domain.append(('name', 'ilike', kwargs['name']))

        offset = int(kwargs.get('offset', 0))
        limit = min(int(kwargs.get('limit', 50)), 100)

        payments = request.env[MODEL_PAYMENT_REFERENCE].sudo().search(
            domain, limit=limit, offset=offset, order='payment_date desc'
        )

        payments = [{
            'date': p.payment_date.strftime('%d/%m/%y') if p.payment_date else '',
            'number': p.name,
            'payment_method': dict(p._fields['payment_type']._description_selection(p.env)).get(p.payment_type, p.payment_type),
            'customer': p.partner_id.name,
            'currency_symbol': p.currency_id.symbol,
            'amount': p.amount,
            'state': p.state,
        } for p in payments]

        return payments

    @http.route('/api/portal/send_payment', type='json', auth="public", csrf=False)
    def sending_payments(self, **kwargs):
        """
        Submit a new payment from the portal user, including optional attachment.

        Parameters (via JSON):
        -----------------------
        - vat: (str) Customer VAT
        - partnerName: (str) Payment owner name
        - date: (str) Payment date (YYYY-MM-DD)
        - bankEmissor: (str) Bank that issued the payment
        - bankReception: (int, optional) ID of the receiving bank
        - ref: (str) Payment reference code
        - paymentType: (str) Payment method ('bank', 'cash', etc.)
        - memo: (str) Payment memo or description
        - amount: (float) Total amount
        - currencyId: (int) Currency ID
        - invoiceName: (str) Associated invoice number
        - observation: (str) Additional observations
        - paymentAttachment: (str, optional) Base64-encoded file content
        - paymentAttachmentName: (str, optional) File name

        Returns:
        ---------
        A JSON response indicating success or failure.
        """
        data = kwargs.get('params', {})
        company_id = request.session.get('selected_company_id') or request.env.company.id

        try:
            # Prepare payment values
            payment_vals = {
                'company_id': company_id,
                'vat': data.get('vat'),
                'partner_id': request.env.user.commercial_partner_id.id,
                'payment_owner': data.get('partnerName'),
                'payment_date': data.get('date'),
                'bank_emissor': data.get('bankEmissor'),
                'payment_reference': data.get('ref'),
                'payment_type': data.get('paymentType'),
                'payment_memo': data.get('memo'),
                'amount': float(data.get('amount', 0.0)),
                'currency_id': int(data.get('currencyId')),
                'invoice_number': data.get('invoiceName'),
                'observation': data.get('observation'),
            }

            # Determine receiving bank
            if data.get('bankReception'):
                payment_vals['bank_receptor'] = int(data.get('bankReception'))
            else:
                journal = request.env['account.journal'].sudo().search([
                    ('company_id', '=', company_id),
                    ('type', '=', data.get('paymentType')),
                    ('currency_id', '=', int(data.get('currencyId'))),
                ], limit=1)
                if journal:
                    payment_vals['bank_receptor'] = journal.id

            # Create payment record
            payment = request.env[MODEL_PAYMENT_REFERENCE].sudo().create(payment_vals)

            # Handle file attachment if provided
            if data.get('paymentAttachment'):
                encoded = base64.b64decode(data['paymentAttachment'].split(',')[1])
                attachment = request.env['ir.attachment'].sudo().create({
                    'name': data.get('paymentAttachmentName'),
                    'type': 'binary',
                    'datas': base64.b64encode(encoded),
                    'res_model': MODEL_PAYMENT_REFERENCE,
                    'res_id': payment.id,
                    'company_id': company_id,
                })
                payment.write({
                    'payment_attachment': attachment.datas,
                    'attachment_id': attachment.id,
                })

            # Generate payment number
            payment.write({'name': payment.get_sequence()})

            return {
                'status': 'success',
                'message': _('Payment successfully registered'),
                'error': False
            }

        except Exception as e:
            _logger.exception('Error while registering payment')
            return {
                'status': 'error',
                'message': _('An error occurred while registering the payment.'),
                'error': str(e)
            }