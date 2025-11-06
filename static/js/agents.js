const API = "http://127.0.0.1:5000/api/agents";

// Variables globales
let currentPage = 1;
const limit = 6;
let totalPages = 1;

/* Load Agents - GET (Paginated) */
async function loadAgents(page = 1) {
  const res = await fetch(`${API}?page=${page}&limit=${limit}`);
  const data = await res.json();

  const tbody = document.querySelector("#agentsTable");
  tbody.innerHTML = "";

  // Render table rows
  data.agents.forEach(a => {
    tbody.innerHTML += `
      <tr>
        <td>${a.agent_id}</td>
        <td>${a.name}</td>
        <td>${a.phone || "-"}</td>
        <td>${a.email}</td>
        <td>
          <button class="btn btn-sm btn-primary edit-btn" data-id="${a.agent_id}">
            <i class="fas fa-edit"></i>
          </button>
          <button class="btn btn-sm btn-danger delete-btn" data-id="${a.agent_id}">
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
  if (currentPage > 1) loadAgents(currentPage - 1);
});

document.getElementById("nextPage").addEventListener("click", () => {
  if (currentPage < totalPages) loadAgents(currentPage + 1);
});

/* Initial load */
loadAgents();

/* Refresh agents list when clicking the "Refresh" button */
const refreshBtn = document.getElementById("refreshBtn");
refreshBtn.addEventListener("click", async () => {
  refreshBtn.classList.add("rotating");
  await loadAgents();
  refreshBtn.classList.remove("rotating");
});

/* --- Add Agent Logic --- */
document.getElementById("agentForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    name: document.getElementById("name").value,
    phone: document.getElementById("phone").value,
    email: document.getElementById("email").value
  };

  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    const addModal = bootstrap.Modal.getInstance(document.getElementById("addAgentModal"));
    addModal.hide();
    loadAgents();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }

  e.target.reset();
});

/* --- Edit Agent Logic --- */

// Detect clicks on Edit buttons
document.addEventListener("click", async (e) => {
  if (e.target.closest(".edit-btn")) {
    const id = e.target.closest(".edit-btn").dataset.id;

    // Fetch agent data by ID
    const res = await fetch(`${API}/${id}`);
    const data = await res.json();
    const agent = data.agent || data;

    // Fill modal fields
    document.getElementById("edit_id").value = agent.agent_id;
    document.getElementById("edit_name").value = agent.name;
    document.getElementById("edit_phone").value = agent.phone || "";
    document.getElementById("edit_email").value = agent.email;

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
    name: document.getElementById("edit_name").value,
    phone: document.getElementById("edit_phone").value,
    email: document.getElementById("edit_email").value
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
  loadAgents();
});

/* --- Delete Agent Logic --- */
let agentToDelete = null;

// Detect clicks on Delete buttons
document.addEventListener("click", (e) => {
  const deleteBtn = e.target.closest(".delete-btn");
  if (deleteBtn) {
    agentToDelete = deleteBtn.dataset.id;
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    deleteModal.show();
  }
});

// Confirm deletion
document.getElementById("confirmDeleteBtn").addEventListener("click", async () => {
  if (!agentToDelete) return;

  const res = await fetch(`${API}/${agentToDelete}`, { method: "DELETE" });
  const deleteModal = bootstrap.Modal.getInstance(document.getElementById("deleteModal"));

  if (res.ok) {
    deleteModal.hide();
    agentToDelete = null;
    loadAgents();

    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});

/* Initial table load */
loadAgents();
