const API_BASE_URL = "http://localhost:8000";

const searchInput = document.querySelector("#customer-search");
const statusFilter = document.querySelector("#status-filter");
const refreshButton = document.querySelector("#refresh-button");
const tableBody = document.querySelector("#invoice-table-body");
const message = document.querySelector("#message");
const lifecycleCustomerSearch = document.querySelector("#lifecycle-customer-search");
const customerTableBody = document.querySelector("#customer-table-body");
const contractTableBody = document.querySelector("#contract-table-body");
const customerContractMessage = document.querySelector("#customer-contract-message");
let customerSearchRequestId = 0;

function formatAmount(amount) {
  return `$${amount.toFixed(2)}`;
}

function setMessage(text, type = "") {
  message.textContent = text;
  message.className = `message ${type}`;
}

function setCustomerContractMessage(text, type = "") {
  customerContractMessage.textContent = text;
  customerContractMessage.className = `message ${type}`;
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
      <td colspan="8">No invoices found</td>
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
      <td>${invoice.customer_id}</td>
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

function renderNoCustomerFound() {
  customerTableBody.innerHTML = `
    <tr>
      <td colspan="4">No customer found</td>
    </tr>
  `;
  contractTableBody.innerHTML = "";
}

function renderCustomer(customer) {
  customerTableBody.innerHTML = "";

  const row = document.createElement("tr");
  row.setAttribute("data-testid", `customer-row-${customer.customer_id}`);
  row.innerHTML = `
    <td>${customer.customer_id}</td>
    <td>${customer.customer_name}</td>
    <td>${customer.customer_type}</td>
    <td>
      <span class="status ${customer.status}">${customer.status}</span>
    </td>
  `;

  customerTableBody.appendChild(row);
}

function renderNoContractFound() {
  contractTableBody.innerHTML = `
    <tr>
      <td colspan="4">No related contract found</td>
    </tr>
  `;
}

function renderContract(contract) {
  contractTableBody.innerHTML = "";

  const row = document.createElement("tr");
  row.setAttribute("data-testid", `contract-row-${contract.contract_id}`);

  const isDraft = contract.status === "Draft";

  row.innerHTML = `
    <td>${contract.contract_id}</td>
    <td>${contract.plan}</td>
    <td>
      <span class="status ${contract.status}">${contract.status}</span>
    </td>
    <td>
      <button
        type="button"
        data-contract-id="${contract.contract_id}"
        ${isDraft ? "" : "disabled"}
      >
        Activate Contract
      </button>
    </td>
  `;

  contractTableBody.appendChild(row);
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

async function findRelatedContractId(customerId) {
  const response = await fetch(
    `${API_BASE_URL}/api/invoices?query=${encodeURIComponent(customerId)}`
  );

  if (!response.ok) {
    return null;
  }

  const invoices = await response.json();
  const invoice = invoices.find((item) => item.customer_id === customerId);

  return invoice ? invoice.contract_id : null;
}

async function loadRelatedContract(customerId, requestId) {
  const contractId = await findRelatedContractId(customerId);

  if (requestId !== customerSearchRequestId) {
    return;
  }

  if (!contractId) {
    renderNoContractFound();
    return;
  }

  const response = await fetch(`${API_BASE_URL}/api/contracts/${contractId}`);

  if (requestId !== customerSearchRequestId) {
    return;
  }

  if (!response.ok) {
    renderNoContractFound();
    return;
  }

  const contract = await response.json();
  renderContract(contract);
}

async function searchCustomer() {
  customerSearchRequestId += 1;
  const requestId = customerSearchRequestId;

  setCustomerContractMessage("");

  const customerId = lifecycleCustomerSearch.value.trim();

  if (!customerId) {
    renderNoCustomerFound();
    return;
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/customers/${encodeURIComponent(customerId)}`
    );

    if (requestId !== customerSearchRequestId) {
      return;
    }

    if (response.status === 404) {
      renderNoCustomerFound();
      return;
    }

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const customer = await response.json();

    renderCustomer(customer);
    await loadRelatedContract(customer.customer_id, requestId);
  } catch (error) {
    if (requestId !== customerSearchRequestId) {
      return;
    }

    renderNoCustomerFound();
    setCustomerContractMessage("Could not load customer from API", "error");
  }
}

async function activateContract(contractId) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/contracts/${contractId}/activate`,
      {
        method: "PATCH",
      }
    );

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const contract = await response.json();
    renderContract(contract);
    setCustomerContractMessage(`${contract.contract_id} was activated`, "success");
  } catch (error) {
    setCustomerContractMessage(`Could not activate contract ${contractId}`, "error");
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

lifecycleCustomerSearch.addEventListener("input", () => {
  searchCustomer();
});

lifecycleCustomerSearch.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    searchCustomer();
  }
});

contractTableBody.addEventListener("click", (event) => {
  const button = event.target.closest("button");

  if (!button) {
    return;
  }

  const contractId = button.dataset.contractId;
  activateContract(contractId);
});

loadInvoices();
