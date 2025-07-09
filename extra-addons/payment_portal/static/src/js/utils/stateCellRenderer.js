/* @odoo-module */

export class StateCellRenderer {
    init(params) {
        this.eGui = document.createElement('span');
        const estado = params.value;

        switch (estado) {
            case 'paid':
                this.eGui.innerHTML = this.getPaidHTML();
                break;
            case 'in_payment':
                this.eGui.innerHTML = this.getProcessPaymentHTML();
                break;
            case 'partial':
                this.eGui.innerHTML = this.getPartialHTML();
                break;
            case 'not_paid':
                this.eGui.innerHTML = this.getUnpaidHTML();
                break;
            case 'confirmed':
                this.eGui.innerHTML = this.getPostedHTML();
                break;
            case 'draft':
                this.eGui.innerHTML = this.getDraftHTML();
                break;
            case 'invalid_payment':
                this.eGui.innerHTML = this.getInvalidPaymentHTML();
                break;
            default:
                this.eGui.innerHTML = this.getUnpaidHTML();
                break;
        }
    }

    getGui() {
        return this.eGui;
    }
    getPaidHTML() {
        return `
            <span class="ag-cell-value ag-portal-cell-value-state--paid">
                <svg xmlns="http://www.w3.org/2000/svg" width="6" height="6" viewBox="0 0 6 6" fill="none">
                    <circle cx="3.00012" cy="3" r="3" fill="#2BBF6D"/>
                </svg> 
                Paid
            </span>`;
    }

    getProcessPaymentHTML() {
        return `
            <span class="ag-cell-value ag-portal-cell-value-state--in-payment">
                <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 11 11" fill="none">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M5.50012 1C3.01484 1 1.00012 3.01472 1.00012 5.5C1.00012 7.98528 3.01484 10 5.50012 10C7.9854 10 10.0001 7.98528 10.0001 5.5C10.0001 3.01472 7.9854 1 5.50012 1ZM0.00012207 5.5C0.00012207 2.46243 2.46256 0 5.50012 0C8.53769 0 11.0001 2.46243 11.0001 5.5C11.0001 8.53757 8.53769 11 5.50012 11C2.46256 11 0.00012207 8.53757 0.00012207 5.5Z" fill="#F1BA67"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M5.50012 2C5.77626 2 6.00012 2.22386 6.00012 2.5V5.58589C6.00012 5.58586 6.00012 5.58593 6.00012 5.58589C6.00018 5.71845 6.05287 5.84567 6.14662 5.93939L7.35368 7.14645C7.54894 7.34171 7.54894 7.65829 7.35368 7.85355C7.15841 8.04882 6.84183 8.04882 6.64657 7.85355L5.43962 6.64661C5.4396 6.64659 5.43964 6.64662 5.43962 6.64661C5.15833 6.36537 5.00021 5.98387 5.00012 5.58611V2.5C5.00012 2.22386 5.22398 2 5.50012 2Z" fill="#F1BA67"/>
                </svg>
                In reconciliation process
            </span>`;
    }

    getPartialHTML() {
        return `
            <span class="ag-cell-value ag-portal-cell-value-state--partial">
                <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 11 11" fill="none">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M5.50012 1C3.01484 1 1.00012 3.01472 1.00012 5.5C1.00012 7.98528 3.01484 10 5.50012 10C7.9854 10 10.0001 7.98528 10.0001 5.5C10.0001 3.01472 7.9854 1 5.50012 1ZM0.00012207 5.5C0.00012207 2.46243 2.46256 0 5.50012 0C8.53769 0 11.0001 2.46243 11.0001 5.5C11.0001 8.53757 8.53769 11 5.50012 11C2.46256 11 0.00012207 8.53757 0.00012207 5.5Z" fill="#E16944"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M5.50012 2C5.77626 2 6.00012 2.22386 6.00012 2.5V5.58589C6.00012 5.58586 6.00012 5.58593 6.00012 5.58589C6.00018 5.71845 6.05287 5.84567 6.14662 5.93939L7.35368 7.14645C7.54894 7.34171 7.54894 7.65829 7.35368 7.85355C7.15841 8.04882 6.84183 8.04882 6.64657 7.85355L5.43962 6.64661C5.4396 6.64659 5.43964 6.64662 5.43962 6.64661C5.15833 6.36537 5.00021 5.98387 5.00012 5.58611V2.5C5.00012 2.22386 5.22398 2 5.50012 2Z" fill="#E16944"/>
                </svg>
                Partially paid
            </span>`;
    }

    getUnpaidHTML() {
        return `
            <span class="ag-cell-value ag-portal-cell-value-state--unpaid">
                <svg xmlns="http://www.w3.org/2000/svg" width="6" height="6" viewBox="0 0 6 6" fill="none">
                    <circle cx="3.00012" cy="3" r="3" fill="#ff0000"/>
                </svg> 
                To pay
            </span>`;
    }

    getPostedHTML() {
        return `
            <span class="ag-cell-value ag-portal-cell-value-state--posted">
                <svg xmlns="http://www.w3.org/2000/svg" width="6" height="6" viewBox="0 0 6 6" fill="none">
                    <circle cx="3.00012" cy="3" r="3" fill="#2BBF6D"/>
                </svg> 
                Confirmed
            </span>`;
    }

    getDraftHTML() {
        return `
            <span class="ag-cell-value ag-portal-cell-value-state--draft">
                <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 11 11" fill="none">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M5.50012 1C3.01484 1 1.00012 3.01472 1.00012 5.5C1.00012 7.98528 3.01484 10 5.50012 10C7.9854 10 10.0001 7.98528 10.0001 5.5C10.0001 3.01472 7.9854 1 5.50012 1ZM0.00012207 5.5C0.00012207 2.46243 2.46256 0 5.50012 0C8.53769 0 11.0001 2.46243 11.0001 5.5C11.0001 8.53757 8.53769 11 5.50012 11C2.46256 11 0.00012207 8.53757 0.00012207 5.5Z" fill="#F1BA67"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M5.50012 2C5.77626 2 6.00012 2.22386 6.00012 2.5V5.58589C6.00012 5.58586 6.00012 5.58593 6.00012 5.58589C6.00018 5.71845 6.05287 5.84567 6.14662 5.93939L7.35368 7.14645C7.54894 7.34171 7.54894 7.65829 7.35368 7.85355C7.15841 8.04882 6.84183 8.04882 6.64657 7.85355L5.43962 6.64661C5.4396 6.64659 5.43964 6.64662 5.43962 6.64661C5.15833 6.36537 5.00021 5.98387 5.00012 5.58611V2.5C5.00012 2.22386 5.22398 2 5.50012 2Z" fill="#F1BA67"/>
                </svg>
                To confirm
            </span>`;
    }

    getInvalidPaymentHTML() {
        return `
            <span class="ag-cell-value ag-portal-cell-value-state--canceled">
                Invalid payment
            </span>`;
    }
}