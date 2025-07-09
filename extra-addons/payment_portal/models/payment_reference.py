# coding: utf-8
##############################################################################
from odoo import fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class PaymentReferencePortalPayment(models.Model):
    _name = 'payment.reference.portal.payment'
    
    name = fields.Char('Payment Number')
    partner_id = fields.Many2one('res.partner', string='Portal User')
    payment_owner = fields.Char('Payment Owner', readonly=1)
    payment_date = fields.Date(string='Payment Date', readonly=1)
    invoice_number = fields.Char(string='Invoice Number', readonly=1)
    payment_type = fields.Selection([
                                        ('deposit', 'Deposit'),
                                        ('transfer', 'Transfer'),
                                        ('cash','Cash')
                                    ],
                                    string='Payment Type',readonly=1)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=1)
    amount = fields.Monetary(string='Amount Paid', currency_field='currency_id')
    vat = fields.Char(string='Identification Number', readonly=1)
    bank_emissor = fields.Char(string='Issuing Bank', readonly=1)
    payment_reference = fields.Char(string='Transaction Reference', readonly=1)
    payment_memo = fields.Char(string='Payment Memo', readonly=1)
    bank_receptor = fields.Many2one('account.journal', string='Receiving Journal/Bank', readonly=1)
    payment_attachment = fields.Binary(string='Attachment File', readonly=1)
    attachment_id = fields.Many2one('ir.attachment', string='Attachment File', readonly=1)
    attachment_name = fields.Char('Attachment Name', related='attachment_id.name', readonly=False)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company, readonly=1, invisible=1)
    state = fields.Selection([('draft', 'Draft'),
                            ('confirmed', 'Confirmed')],
                            string='Payment Status',
                            default='draft',
                            readonly=True
                            )
    observation = fields.Text(string='Observation')
    payment_ids = fields.Many2many('account.payment', string='Payments', domain="[('state', 'in', ['paid', 'in_process']),('partner_id', '=', partner_id)]")

    def action_confirm(self):
        """
        Confirm the record only if at least one payment is registered.

        Raises:
        -------
        UserError if no payments are linked to the record.
        """
        for rec in self:
            if rec.payment_ids:
                rec.state = 'confirmed'
            else:
                raise UserError(_('At least one payment must be registered before confirming.'))

    def action_draft(self):
        """
        Reset the record state to 'draft' if it has linked payments.
        """
        for rec in self:
            if rec.payment_ids:
                rec.state = 'draft'

    def get_sequence(self):
        """
        Generate a monthly sequence number for the record, formatted with the current month.

        Returns:
        --------
        str: The formatted sequence string (e.g., REF/2024/07/0001)

        Notes:
        ------
        - Uses monthly date ranges in ir.sequence.
        - Inserts the padded month (MM) into the generated code.
        """
        main_sequence = self.env['ir.sequence'].search([
            ('code', '=', 'payment.reference.portal.payment')
        ])

        date = datetime.strptime(str(self.payment_date), '%Y-%m-%d')
        initial_date = date.replace(day=1).date()
        last_date_of_month = (date.replace(day=1) + relativedelta(months=1, days=-1)).date()

        subsequences = main_sequence.date_range_ids

        # Use existing subsequence if available
        existing = subsequences.filtered(lambda line: line.date_from == initial_date)
        if existing:
            name = existing.with_context(ir_sequence_date_range=last_date_of_month)._next()
        else:
            # Create a new subsequence for the month
            new_subsequence = self.env['ir.sequence.date_range'].create({
                'date_from': initial_date,
                'date_to': last_date_of_month,
                'sequence_id': main_sequence.id,
                'number_next': 1,
            })
            name = new_subsequence.with_context(ir_sequence_date_range=last_date_of_month)._next()

        # Inject the month into the generated name
        month = str(date.month).zfill(2)
        name = name[:13] + month + name[15:]
        return name