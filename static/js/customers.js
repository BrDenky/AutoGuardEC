const API = "http://127.0.0.1:5000/api/customers";

// Variables globales
let currentPage = 1;
const limit = 6;
let totalPages = 1;

/* Load Customers - GET (Paginated) */
async function loadCustomers(page = 1) {
  const res = await fetch(`${API}?page=${page}&limit=${limit}`);
  const data = await res.json();

  const tbody = document.querySelector("#customersTable");
  tbody.innerHTML = "";

  // Render table rows
  data.customers.forEach(c => {
    tbody.innerHTML += `
      <tr>
        <td>${c.customer_id}</td>
        <td>${c.first_name}</td>
        <td>${c.last_name}</td>
        <td>${c.address}</td>
        <td>${c.phone}</td>
        <td>${c.email}</td>
        <td>
          <button class="btn btn-sm btn-primary edit-btn" data-id="${c.customer_id}">
            <i class="fas fa-edit"></i>
          </button>
          <button class="btn btn-sm btn-danger delete-btn" data-id="${c.customer_id}">
            <i class="fas fa-trash-alt"></i>
          </button>
        </td>
      </tr>`;
  });

  // Update pagination info
  currentPage = data.current_page;
  totalPages = data.total_pages;

  document.getElementById("pageInfo").textContent = `Page ${currentPage} of ${totalPages}`;

  // Enable/disable navigation buttons
  document.getElementById("prevPage").disabled = !data.has_prev;
  document.getElementById("nextPage").disabled = !data.has_next;
}

/* Pagination button handlers */
document.getElementById("prevPage").addEventListener("click", () => {
  if (currentPage > 1) loadCustomers(currentPage - 1);
});

document.getElementById("nextPage").addEventListener("click", () => {
  if (currentPage < totalPages) loadCustomers(currentPage + 1);
});

/* Initial load */
loadCustomers();


/* Refresh customers list when clicking the "Refresh" button */
const refreshBtn = document.getElementById("refreshBtn");
refreshBtn.addEventListener("click", async () => {
  refreshBtn.classList.add("rotating");
  await loadCustomers();
  refreshBtn.classList.remove("rotating");
});

/* EDIT Customer */



/* --- Edit Customer Logic --- */

// Detect clicks on Edit buttons
document.addEventListener("click", async (e) => {
  if (e.target.closest(".edit-btn")) {
    const id = e.target.closest(".edit-btn").dataset.id;

    // Fetch customer data by ID
    const res = await fetch(`${API}/${id}`);
    const data = await res.json();
    const customer = data.customer || data;

    // Fill modal fields
    document.getElementById("edit_id").value = customer.customer_id;
    document.getElementById("edit_first_name").value = customer.first_name;
    document.getElementById("edit_last_name").value = customer.last_name;
    document.getElementById("edit_email").value = customer.email;
    document.getElementById("edit_phone").value = customer.phone;
    document.getElementById("edit_address").value = customer.address;

    // Show modal
    const editModal = new bootstrap.Modal(document.getElementById("editModal"));
    editModal.show();
  }
});

// Handle form submission for updates
document.getElementById("editForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = document.getElementById("edit_id").value;

  const payload = {
    first_name: document.getElementById("edit_first_name").value,
    last_name: document.getElementById("edit_last_name").value,
    email: document.getElementById("edit_email").value,
    phone: document.getElementById("edit_phone").value,
    address: document.getElementById("edit_address").value
  };

  await fetch(`${API}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  // Close modal
  const editModal = bootstrap.Modal.getInstance(document.getElementById("editModal"));
  editModal.hide();

  // Refresh table
  loadCustomers();
});



/* --- Delete Customer Logic --- */
let customerToDelete = null;
// Detect clicks on Delete buttons
document.addEventListener("click", (e) => {
  const deleteBtn = e.target.closest(".delete-btn");
  if (deleteBtn) {
    customerToDelete = deleteBtn.dataset.id; // Guarda el id temporalmente
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    deleteModal.show(); // Muestra el modal
  }
});
// Confirm deletion when user clicks "Delete" in modal
document.getElementById("confirmDeleteBtn").addEventListener("click", async () => {
  if (!customerToDelete) return;

  const res = await fetch(`${API}/${customerToDelete}`, { method: "DELETE" });
  const deleteModal = bootstrap.Modal.getInstance(document.getElementById("deleteModal"));

  if (res.ok) {
  deleteModal.hide();
  customerToDelete = null;
  loadCustomers();

  const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
  toast.show();
} else {
  const toast = new bootstrap.Toast(document.getElementById("toastError"));
  toast.show();
}
});






loadCustomers();
