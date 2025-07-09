# -*- coding: utf-8 -*-

import odoo
from odoo import models, api
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @api.model
    def get_frontend_session_info(self):
        """
        Extend default session info with custom data for the payment portal.

        Returns:
        ---------
        dict: Updated session information including:
            - user_name: (str) Logged-in user's full name
            - user_email: (str) Email or login of the user
            - is_user_portal_payment: (bool) Whether user has portal payment access
            - company_name: (str) Name of the selected company from session
        """
        session_info = super().get_frontend_session_info()

        session_info.update({
            'user_name': request.env.user.name,
            'user_email': request.env.user.email or request.env.user.login,
            'is_user_portal_payment': request.env.user.is_user_portal_payment,
            'company_name': request.env['res.company'].sudo().search([
                ('id', '=', request.session.get('selected_company_id', False))
            ]).name
        })

        return session_info