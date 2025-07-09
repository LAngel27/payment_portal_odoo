/* @odoo-module */

import { Component } from '@odoo/owl';


export class Navbar extends Component {
    static template = 'payment_portal.Navbar';
    static components = {};
    static props = {
        title: { type: String, optional: true, default: 'Portal Payment'},
        userName: { type: String },
        userEmail: { type: String },
        companyName: { type: String },
    }
}