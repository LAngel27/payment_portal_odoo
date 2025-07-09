from odoo import _, api, fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    show_payment_portal = fields.Boolean(string='Show Portal Payment')
