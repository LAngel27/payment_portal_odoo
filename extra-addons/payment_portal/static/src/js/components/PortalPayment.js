/* @odoo-module */
import { Component, onWillStart, useState, useRef, mount, whenReady, onMounted } from '@odoo/owl';
import { translations } from '../utils/ag-grid-translations';
import { session } from '@web/session';
import { Navbar } from './Navbar';
import { getTemplate } from "@web/core/templates";
import { ModalPayment } from './ModalPayment';
import { StateCellRenderer } from '../utils/stateCellRenderer';
import { rpc } from "@web/core/network/rpc";
import { globalEventBusPortalPayment } from '../utils/global_events_payment_portal';

export class PortalPayment extends Component {
    static template = 'payment_portal.PortalPayment';
    static components = { Navbar, ModalPayment };

    /**
     * Setup state, refs and lifecycle hooks.
     */
    setup () {
        super.setup();

        this.state = useState({
            titleSection: 'Facturas Recibidas',
            userName: session.user_name,
            userEmail: session.user_email,
            companyName: session.company_name,
            view: 'invoices',
            data: [],
            filterName: '',
            dateFilter: '',
            filterState: '',
            showPaymentButton: false,
            references: false,
            openFilterState: false,
            isGridReady: false,
            grid: null,
        });

        this.refInputSearchName = useRef('inputSearchName');
        this.refInputSearchDate = useRef('inputSearchDate');
        this.rpc = rpc;

        onWillStart(() => this._fetchAndRenderData());
        onMounted(() => this._initializeGrid(this._getGridSelector()));
    }

    /**
     * Get the API route depending on current view (invoices or payments).
     */
    _getApiRoute() {
        return this.state.view === 'invoices' ? '/api/portal/invoices' : '/api/portal/payments';
    }

    /**
     * Get the DOM selector for the current grid container.
     */
    _getGridSelector() {
        return this.state.view === 'invoices' ? '#invoices' : '#payments';
    }

    /**
     * Build search params based on current filters and view.
     */
    _buildParams() {
        return {
            name: this.state.filterName,
            date: this.state.dateFilter,
            [this.state.view === 'invoices' ? 'payment_state' : 'state']: this.state.filterState,
            expired_invoice: this.state.filterState === 'defeated',
            current_invoice: this.state.filterState === 'current',
        };
    }

    /**
     * Reset all search filters and dropdowns.
     */
    _resetFilters() {
        this.state.filterName = '';
        this.state.dateFilter = '';
        this.state.filterState = '';
        this.state.openFilterState = false;
    }

    /**
     * Apply fetched data to the ag-Grid dynamically.
     */
    _applyDataToGrid(data) {
        this.state.data = data;

        if (!this.gridApi?.applyTransaction) {
            setTimeout(() => this._applyDataToGrid(data), 100);
            return;
        }

        this.clearAllRows();
        this.gridApi.applyTransaction({ add: data });
    }

    /**
     * Fetch data from the API and optionally return it for further handling.
     */
    async _fetchAndRenderData(params = {}, returnData = false) {
        try {
            const data = await this.rpc(this._getApiRoute(), { params });
            if (returnData) return data;
            this._applyDataToGrid(data);
        } catch (error) {
            console.error(error);
        }
    }

    /**
     * Remove all current rows from the grid.
     */
    clearAllRows() {
        if (!this.gridApi?.forEachNode) return;

        const nodesToRemove = [];
        this.gridApi.forEachNode(node => node?.data && nodesToRemove.push(node.data));
        if (nodesToRemove.length) {
            this.gridApi.applyTransaction({ remove: nodesToRemove });
        }
    }

    /**
     * Initialize ag-Grid instance with column definitions and events.
     */
    _initializeGrid(selector) {
        const gridOptions = {
            columnDefs: this._getColumnDefs(),
            rowData: this.state.data,
            defaultColDef: { filter: false, floatingFilter: false },
            pagination: true,
            paginationPageSize: 25,
            rowHeight: 60,
            rowSelection: 'multiple',
            suppressRowClickSelection: true,
            localeText: translations['es'],

            onGridReady: ({ api, columnApi }) => {
                this.gridApi = api;
                this.gridColumnApi = columnApi;
                this.state.isGridReady = true;
            },

            onPaginationChanged: async () => {
                const currentPage = this.gridApi?.paginationGetCurrentPage?.();
                const totalPages = this.gridApi?.paginationGetTotalPages?.();

                if (currentPage === totalPages - 1 && totalPages > 1) {
                    await this._loadMoreData();
                }
            },

            onSelectionChanged: () => {
                const selected = this.gridApi?.getSelectedRows()?.filter(row => row.state !== 'paid') || [];
                this.state.showPaymentButton = !!selected.length;
                this.state.references = selected.length ? selected.map(r => r.number).join(', ') : false;
                globalEventBusPortalPayment.trigger('updateInvoiceName', this.state.references);
            },

            onRowSelected: ({ node }) => {
                if (node.isSelected() && node.data.state === 'paid') {
                    node.setSelected(false);
                }
            },
        };

        const container = document.querySelector(selector);
        if (container) {
            this.grid = agGrid.createGrid(container, gridOptions);
            this.state.grid = this.grid;
        }
    }

    /**
     * Define ag-Grid column structure depending on current view.
     */
    _getColumnDefs() {
        if (this.state.view === 'invoices') {
            return [
            {
                headerName: "", width: 50, checkboxSelection: ({ data }) => data.state !== 'paid',
                suppressRowClickSelection: true, headerCheckboxSelection: true
            },
            { headerName: "Invoice Number", field: "number", flex: 1 },
            { headerName: "Date", field: "date", flex: 1 },
            {
                headerName: "Total Due", field: "amount_residual", flex: 1,
                valueFormatter: ({ value }) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
            },
            { headerName: "State", field: "state", cellRenderer: StateCellRenderer, flex: 1 },
            ];
        }
        return [
            { headerName: "Date", field: "date", flex: 1 },
            { headerName: "Number", field: "number", flex: 1 },
            { headerName: "Payment Method", field: "payment_method", flex: 1 },
            { headerName: "Customer", field: "customer", flex: 1 },
            { headerName: "Currency", field: "currency_symbol", flex: 1 },
            { headerName: "Amount", field: "amount", flex: 1 },
            { headerName: "State", field: "state", cellRenderer: StateCellRenderer, flex: 1 },
        ];
    }

    /**
     * Load additional data (next page) when paginating to the end.
     */
    async _loadMoreData() {
        const offset = this.state.data.length;
        const newData = await this._fetchAndRenderData({
            ...this._buildParams(),
            offset,
            limit: 50,
        }, true);

        if (Array.isArray(newData)) {
            this.state.data = [...this.state.data, ...newData];
            this.gridApi.applyTransaction({ add: newData });
        }
    }

    /**
     * Switch view to invoices and reload grid.
     */
    async _onClickViewInvoices() {
        if (this.state.view !== 'invoices') {
            this.state.view = 'invoices';
            this.state.titleSection = 'Facturas Recibidas';
            this.state.showPaymentButton = false;
            this._resetFilters();
            await this._fetchAndRenderData();
            this._initializeGrid('#invoices');
        }
    }

    /**
     * Switch view to payments and reload grid.
     */
    async _onClickViewPayments() {
        if (this.state.view !== 'payments') {
            this.state.view = 'payments';
            this.state.titleSection = 'Pagos Recibidos';
            this.state.showPaymentButton = true;
            this._resetFilters();
            await this._fetchAndRenderData();
            this._initializeGrid('#payments');
        }
    }

    /**
     * Trigger search when date input is changed.
     */
    async _onChangeDate() {
        this.state.dateFilter = this.refInputSearchDate.el.value;
        const data = await this._fetchAndRenderData(this._buildParams(), true);
        this._applyDataToGrid(data);
    }

    /**
     * Trigger search when name filter is used.
     */
    async _onClickSearchName() {
        this.state.filterName = this.refInputSearchName.el.value;
        const data = await this._fetchAndRenderData(this._buildParams(), true);
        this._applyDataToGrid(data);
    }

    /**
     * Toggle dropdown filter for invoice/payment state.
     */
    _onToggleDropdown(ev) {
        ev.stopPropagation();
        this.state.openFilterState = !this.state.openFilterState;
    }

    /**
     * Select a specific invoice/payment state from dropdown.
     */
    async _onClickItemState(ev) {
        const value = ev.target.dataset.value;
        this.state.filterState = this.state.filterState === value ? '' : value;
        const data = await this._fetchAndRenderData(this._buildParams(), true);
        this._applyDataToGrid(data);
    }
}

/**
 * Mount PortalPayment component when DOM is ready.
 */
whenReady(async () => {
    const mountTarget = document.querySelector('#portal-payment');
    if (mountTarget) {
        await mount(PortalPayment, mountTarget, { getTemplate });
    }
});
