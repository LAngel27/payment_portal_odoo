/* @odoo-module */

import { Component, onWillStart, useState, useRef, onMounted, useExternalListener } from '@odoo/owl';
import { globalEventBusPortalPayment } from '../utils/global_events_payment_portal';
import { rpc } from "@web/core/network/rpc";

export class ModalPayment extends Component {
    static template = 'payment_portal.ModalPayment';
    static props = {
        view: { type: String },
    };

    /**
     * Setup state, refs, event listeners and lifecycle.
     */
    setup() {
        this.state = useState({
            banks: [],
            currencies: [],
            partnerName: '',
            date: '',
            invoiceName: '',
            paymentType: '',
            amount: '',
            currencyId: '',
            vat: '',
            emissorBank: '',
            emissorBankSelected: '',
            ref: '',
            bankReception: '',
            memo: '',
            paymentAttachment: false,
            paymentAttachmentName: '',
            paymentSend: false,
            paymentSendError: false,
            observation: '',
            showLoader: false,
        });

        this.rpc = rpc;
        this.form = useRef('formSendPayment');
        this.attachmentInput = useRef('attachmentSpan');
        this.bankEmissor = useRef('bankEmissor');
        this.reference = useRef('reference');
        this.bankReception = useRef('bankReception');
        this.modalRef = useRef('modalPayment');

        // Listen for global event to update invoice reference
        useExternalListener(globalEventBusPortalPayment, "updateInvoiceName", this.updateInvoiceName);

        // Load banks and currencies before render
        onWillStart(async () => {
            await this._fechData('/api/portal/currencies');
            await this._fechData('/api/portal/banks');
        });

        // Reset modal state on modal open
        onMounted(() => {
            this.modalRef.el.addEventListener('show.bs.modal', () => {
                this._onChangeToBlankState();
            });
        });
    }

    /**
     * Send payment to the backend via RPC if form is valid.
     */
    async _onClickSendPayment(ev) {
        ev.preventDefault();

        if (!this.form.el.checkValidity()) {
            this.form.el.reportValidity();
            return;
        }

        this.state.showLoader = true;
        try {
            const result = await this.rpc('/api/portal/send_payment', {
                params: {
                    banks: this.state.banks,
                    currencies: this.state.currencies,
                    partnerName: this.state.partnerName,
                    date: this.state.date,
                    invoiceName: this.state.invoiceName,
                    paymentType: this.state.paymentType,
                    amount: this.state.amount,
                    currencyId: this.state.currencyId,
                    vat: this.state.vat,
                    bankEmissor: this.state.emissorBankSelected,
                    ref: this.state.ref,
                    bankReception: this.state.bankReception,
                    memo: this.state.memo,
                    paymentAttachment: this.state.paymentAttachment,
                    paymentAttachmentName: this.state.paymentAttachmentName,
                    observation: this.state.observation,
                },
            });

            if (result?.status === 'success') {
                this.state.paymentSend = true;
                setTimeout(() => window.location.reload(), 1000);
            } else {
                throw new Error(result.error);
            }
        } catch (error) {
            this.state.paymentSendError = true;
            console.error(error);
        } finally {
            this.state.showLoader = false;
        }
    }

    /**
     * Update invoice reference name from global event.
     */
    updateInvoiceName({ detail }) {
        this.state.invoiceName = detail;
    }

    // Handlers for input changes (basic 1:1 updates)
    _onChangePartner(ev) { this.state.partnerName = ev.target.value; }
    _onChangeDate(ev) { this.state.date = ev.target.value; }
    _onChangeInvoiceName(ev) { this.state.invoiceName = ev.target.value; }
    _onChangeMemo(ev) { this.state.memo = ev.target.value; }
    _onChangeRef(ev) { this.state.ref = ev.target.value; }
    _onChangeObservation(ev) { this.state.observation = ev.target.value; }
    _onChangeVat(ev) { this.state.vat = ev.target.value; }
    _onChangeBankReception(ev) { this.state.bankReception = ev.target.value; }
    _onChangeCurrencyId(ev) { this.state.currencyId = ev.target.value; }
    _onChangeEmissorBank(ev) { this.state.emissorBankSelected = ev.target.value; }

    /**
     * Handle payment type selection.
     */
    async _onChangePaymentType(ev) {
        this.state.paymentType = ev.target.value;
        this.state.filteredCurrencies = this.state.currencies;
    }

    /**
     * Handle payment amount input and sanitize format.
     */
    _onChangeAmount(ev) {
        let input = ev.currentTarget.value;
        if (input == '0') input = '';
        else {
            const parts = input.split('.');
            input = parts.length > 1 ? `${parts[0]}.${parts.slice(1).join('')}` : parts[0];
            let numericValue = Math.abs(parseFloat(input) || 0).toString();
            if (numericValue.includes('.')) {
                const [intPart, decPart] = numericValue.split('.');
                input = `${intPart}.${decPart.slice(0, 2)}`;
            }
        }
        this.state.amount = input;
    }

    /**
     * Handle file upload and read as base64.
     */
    _onChangePaymentAttachment(ev) {
        const files = ev.target.files;
        if (files.length) {
            const file = files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                this.state.paymentAttachment = e.target.result;
                this.state.paymentAttachmentName = file.name;
            };
            reader.readAsDataURL(file);
        }
    }

    /**
     * Reset modal state when opened.
     */
    _onChangeToBlankState() {
        Object.assign(this.state, {
            partnerName: '',
            date: '',
            paymentType: '',
            currencyId: '',
            vat: '',
            emisorBank: '',
            ref: '',
            bankReception: '',
            paymentAttachment: false,
            paymentSend: false,
            paymentSendError: false,
            amount: '',
            showLoader: false,
        });
    }

    /**
     * Fetch banks or currencies from backend based on endpoint.
     */
    async _fechData(url) {
        try {
            const data = await this.rpc(url, { params: {} });
            const key = url.split('/').pop();
            this.state[key] = data;
        } catch (error) {
            console.error(error);
        }
    }
}
