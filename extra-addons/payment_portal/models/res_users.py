# -*- coding: utf-8 -*-

from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_user_portal_payment = fields.Boolean(string='User Portal Payment', default=False)