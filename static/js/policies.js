const API = "http://127.0.0.1:5000/api/policies";

// Variables globales
let currentPage = 1;
const limit = 6;
let totalPages = 1;

/* Load Policies - GET (Paginated) */
async function loadPolicies(page = 1) {
  const res = await fetch(`${API}?page=${page}&limit=${limit}`);
  const data = await res.json();

  const tbody = document.querySelector("#policiesTable");
  tbody.innerHTML = "";
  // Render table rows with status badges
  data.policies.forEach(p => {
    // Determinar color del badge según el status
    let statusBadge = '';
    switch(p.status.toLowerCase()) {
      case 'active':
        statusBadge = `<span class="badge bg-success badge-fixed-width">${p.status}</span>`;
        break;
      case 'expired':
        statusBadge = `<span class="badge bg-secondary badge-fixed-width">${p.status}</span>`;
        break;
      case 'canceled':
        statusBadge = `<span class="badge bg-danger badge-fixed-width">${p.status}</span>`;
        break;
      case 'arrears':
        statusBadge = `<span class="badge bg-warning text-dark badge-fixed-width">${p.status}</span>`;
        break;
      default:
        statusBadge = `<span class="badge bg-info badge-fixed-width">${p.status}</span>`;
    }

    tbody.innerHTML += `
      <tr>
        <td>${p.policy_id}</td>
        <td>
          <button class="btn btn-link p-0 customer-qv-btn" data-id="${p.customer_id}">
            ${p.customer_id}
          </button>
        </td>
        <td>
          <button class="btn btn-link p-0 vehicle-qv-btn" data-id="${p.vehicle_id}">
            ${p.vehicle_id}
          </button>
        </td>
        <td>
          <button class="btn btn-link p-0 agent-qv-btn" data-id="${p.agent_id}">
            ${p.agent_id}
          </button>
        </td>
        <td>${p.start_date}</td>
        <td>${p.end_date}</td>
        <td>${statusBadge}</td>
        <td>
          <button class="btn btn-sm btn-primary edit-btn" data-id="${p.policy_id}">
            <i class="fas fa-edit"></i>
          </button>
          <button class="btn btn-sm btn-danger delete-btn" data-id="${p.policy_id}">
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
  if (currentPage > 1) loadPolicies(currentPage - 1);
});

document.getElementById("nextPage").addEventListener("click", () => {
  if (currentPage < totalPages) loadPolicies(currentPage + 1);
});

/* Initial load */
loadPolicies();

/* Refresh policies list when clicking the "Refresh" button */
const refreshBtn = document.getElementById("refreshBtn");
refreshBtn.addEventListener("click", async () => {
  refreshBtn.classList.add("rotating");
  await loadPolicies(currentPage);
  refreshBtn.classList.remove("rotating");
});

/* --- Add Policy Logic --- */
document.getElementById("policyForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const payload = {
    customer_id: parseInt(document.getElementById("customer_id").value),
    vehicle_id: parseInt(document.getElementById("vehicle_id").value),
    agent_id: parseInt(document.getElementById("agent_id").value),
    start_date: document.getElementById("start_date").value,
    end_date: document.getElementById("end_date").value,
    status: document.getElementById("status").value
  };

  await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  // Close modal
  const addModal = bootstrap.Modal.getInstance(document.getElementById("addPolicyModal"));
  addModal.hide();

  // Reset form
  document.getElementById("policyForm").reset();

  // Refresh table
  loadPolicies(currentPage);
});

/* --- Edit Policy Logic --- */

// Detect clicks on Edit buttons
document.addEventListener("click", async (e) => {
  if (e.target.closest(".edit-btn")) {
    const id = e.target.closest(".edit-btn").dataset.id;

    // Fetch policy data by ID
    const res = await fetch(`${API}/${id}`);
    const data = await res.json();
    const policy = data.policy || data;

    // Fill modal fields
    document.getElementById("edit_id").value = policy.policy_id;
    document.getElementById("edit_customer_id").value = policy.customer_id;
    document.getElementById("edit_vehicle_id").value = policy.vehicle_id;
    document.getElementById("edit_agent_id").value = policy.agent_id;
    document.getElementById("edit_start_date").value = policy.start_date;
    document.getElementById("edit_end_date").value = policy.end_date;
    document.getElementById("edit_status").value = policy.status;

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
    customer_id: parseInt(document.getElementById("edit_customer_id").value),
    vehicle_id: parseInt(document.getElementById("edit_vehicle_id").value),
    agent_id: parseInt(document.getElementById("edit_agent_id").value),
    start_date: document.getElementById("edit_start_date").value,
    end_date: document.getElementById("edit_end_date").value,
    status: document.getElementById("edit_status").value
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
  loadPolicies(currentPage);
});

/* --- Delete Policy Logic --- */
let policyToDelete = null;

// Detect clicks on Delete buttons
document.addEventListener("click", (e) => {
  const deleteBtn = e.target.closest(".delete-btn");
  if (deleteBtn) {
    policyToDelete = deleteBtn.dataset.id;
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    deleteModal.show();
  }
});

// Confirm deletion when user clicks "Delete" in modal
document.getElementById("confirmDeleteBtn").addEventListener("click", async () => {
  if (!policyToDelete) return;

  const res = await fetch(`${API}/${policyToDelete}`, { method: "DELETE" });
  const deleteModal = bootstrap.Modal.getInstance(document.getElementById("deleteModal"));

  if (res.ok) {
    deleteModal.hide();
    policyToDelete = null;
    loadPolicies(currentPage);

    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});