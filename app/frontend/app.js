const API_BASE_URL = "http://localhost:8000";

const searchInput = document.querySelector("#customer-search");
const statusFilter = document.querySelector("#status-filter");
const refreshButton = document.querySelector("#refresh-button");
const tableBody = document.querySelector("#invoice-table-body");
const message = document.querySelector("#message");

function formatAmount(amount) {
  return `$${amount.toFixed(2)}`;
}

function setMessage(text, type = "") {
  message.textContent = text;
  message.className = `message ${type}`;
}

function buildQueryParams() {
  const params = new URLSearchParams();

  const query = searchInput.value.trim();
  const status = statusFilter.value;

  if (query) {
    params.set("query", query);
  }

  if (status) {
    params.set("status", status);
  }

  return params.toString();
}

function renderInvoices(invoices) {
  tableBody.innerHTML = "";

  if (invoices.length === 0) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td colspan="7">No invoices found</td>
    `;
    tableBody.appendChild(row);
    return;
  }

  invoices.forEach((invoice) => {
    const row = document.createElement("tr");
    row.setAttribute("data-testid", `invoice-row-${invoice.invoice_id}`);

    const isPaid = invoice.status === "Paid";

    row.innerHTML = `
      <td>${invoice.invoice_id}</td>
      <td>${invoice.customer_name}</td>
      <td>${invoice.contract_id}</td>
      <td>${invoice.plan}</td>
      <td>${formatAmount(invoice.amount)}</td>
      <td>
        <span class="status ${invoice.status}">${invoice.status}</span>
      </td>
      <td>
        <button
          type="button"
          data-invoice-id="${invoice.invoice_id}"
          ${isPaid ? "disabled" : ""}
        >
          Mark as Paid
        </button>
      </td>
    `;

    tableBody.appendChild(row);
  });
}

async function loadInvoices() {
  setMessage("");

  const queryString = buildQueryParams();
  const url = queryString
    ? `${API_BASE_URL}/api/invoices?${queryString}`
    : `${API_BASE_URL}/api/invoices`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const invoices = await response.json();
    renderInvoices(invoices);
  } catch (error) {
    renderInvoices([]);
    setMessage("Could not load invoices from API", "error");
  }
}

async function markInvoiceAsPaid(invoiceId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/invoices/${invoiceId}/pay`, {
      method: "PATCH",
    });

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const invoice = await response.json();

    await loadInvoices();
    setMessage(`${invoice.invoice_id} was marked as paid`, "success");
  } catch (error) {
    setMessage(`Could not update invoice ${invoiceId}`, "error");
  }
}

searchInput.addEventListener("input", () => {
  loadInvoices();
});

statusFilter.addEventListener("change", () => {
  loadInvoices();
});

refreshButton.addEventListener("click", () => {
  loadInvoices();
});

tableBody.addEventListener("click", (event) => {
  const button = event.target.closest("button");

  if (!button) {
    return;
  }

  const invoiceId = button.dataset.invoiceId;
  markInvoiceAsPaid(invoiceId);
});

loadInvoices();