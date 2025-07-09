from odoo import api, models, fields


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    value = fields.Text(required=False)