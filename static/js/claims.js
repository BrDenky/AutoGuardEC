const API = "http://127.0.0.1:5000/api/claims";

// Global vars
let currentPage = 1;
const limit = 6;
let totalPages = 1;

/* =======================================
   LOAD CLAIMS (GET PAGINATED)
======================================= */
async function loadClaims(page = 1) {
  const res = await fetch(`${API}?page=${page}&limit=${limit}`);
  const data = await res.json();

  const tbody = document.querySelector("#claimsTable");
  tbody.innerHTML = "";

  // Render rows with status badges
  data.claims.forEach(c => {

    // Badge based on claim status
    let statusBadge = "";
    switch (c.status.toLowerCase()) {

      case "open":
        statusBadge = `<span class="badge bg-success badge-fixed-width">${c.status}</span>`;
        break;

      case "in review":
        statusBadge = `<span class="badge bg-warning text-dark badge-fixed-width">${c.status}</span>`;
        break;

      case "closed":
        statusBadge = `<span class="badge bg-secondary badge-fixed-width">${c.status}</span>`;
        break;

      default:
        statusBadge = `<span class="badge bg-info badge-fixed-width">${c.status}</span>`;
    }

    tbody.innerHTML += `
      <tr>
        <td>${c.claim_id}</td>
        <td>
          <button class="btn btn-link p-0 policy-qv-btn" data-id="${c.policy_id}">
            ${c.policy_id}
          </button>
        </td>
        <td>${c.claim_date}</td>
        <td>${c.description}</td>
        <td>${statusBadge}</td>
        <td>
          <button class="btn btn-sm btn-primary edit-btn" data-id="${c.claim_id}">
            <i class="fas fa-edit"></i>
          </button>

          <button class="btn btn-sm btn-danger delete-btn" data-id="${c.claim_id}">
            <i class="fas fa-trash-alt"></i>
          </button>
        </td>
      </tr>`;
  })

  // Update pagination info
  currentPage = data.current_page;
  totalPages = data.total_pages;

  document.getElementById("pageInfo").textContent =
    `Page ${currentPage} of ${totalPages}`;

  document.getElementById("prevPage").disabled = !data.has_prev;
  document.getElementById("nextPage").disabled = !data.has_next;
}


/* =======================================
   PAGINATION BUTTONS
======================================= */
document.getElementById("prevPage").addEventListener("click", () => {
  if (currentPage > 1) loadClaims(currentPage - 1);
});

document.getElementById("nextPage").addEventListener("click", () => {
  if (currentPage < totalPages) loadClaims(currentPage + 1);
});


/* =======================================
   REFRESH BUTTON
======================================= */
const refreshBtn = document.getElementById("refreshBtn");
refreshBtn.addEventListener("click", async () => {
  refreshBtn.classList.add("rotating");
  await loadClaims();
  refreshBtn.classList.remove("rotating");
});


/* =======================================
   ADD CLAIM (POST)
======================================= */
document.getElementById("claimForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    policy_id: document.getElementById("policy_id").value,
    claim_date: document.getElementById("claim_date").value,
    description: document.getElementById("description").value,
    status: document.getElementById("status").value
  };

  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    bootstrap.Modal.getInstance(document.getElementById("addClaimModal")).hide();
    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();
    loadClaims();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }

  e.target.reset();
});


/* =======================================
   EDIT CLAIM — OPEN MODAL
======================================= */
document.addEventListener("click", async (e) => {
  if (e.target.closest(".edit-btn")) {
    const id = e.target.closest(".edit-btn").dataset.id;

    const res = await fetch(`${API}/${id}`);
    const data = await res.json();
    const c = data.claim || data;

    // Fill modal fields
    document.getElementById("edit_id").value = c.claim_id;
    document.getElementById("edit_policy_id").value = c.policy_id;
    document.getElementById("edit_claim_date").value = c.claim_date;
    document.getElementById("edit_description").value = c.description;
    document.getElementById("edit_status").value = c.status;

    // Show modal
    const editModal = new bootstrap.Modal(document.getElementById("editModal"));
    editModal.show();
  }
});


/* =======================================
   UPDATE CLAIM (PUT)
======================================= */
document.getElementById("editForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = document.getElementById("edit_id").value;

  const payload = {
    policy_id: document.getElementById("edit_policy_id").value,
    claim_date: document.getElementById("edit_claim_date").value,
    description: document.getElementById("edit_description").value,
    status: document.getElementById("edit_status").value
  };

  const res = await fetch(`${API}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const editModal = bootstrap.Modal.getInstance(document.getElementById("editModal"));
  editModal.hide();

  if (res.ok) {
    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();
    loadClaims();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});


/* =======================================
   DELETE CLAIM (CONFIRM MODAL)
======================================= */
let claimToDelete = null;

document.addEventListener("click", (e) => {
  const btn = e.target.closest(".delete-btn");
  if (btn) {
    claimToDelete = btn.dataset.id;
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    deleteModal.show();
  }
});

document.getElementById("confirmDeleteBtn").addEventListener("click", async () => {
  if (!claimToDelete) return;

  const res = await fetch(`${API}/${claimToDelete}`, {
    method: "DELETE"
  });

  const deleteModal = bootstrap.Modal.getInstance(document.getElementById("deleteModal"));

  if (res.ok) {
    deleteModal.hide();
    claimToDelete = null;
    loadClaims();

    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});


/* INITIAL LOAD */
loadClaims();
