const API = "http://127.0.0.1:5000/api/policy_coverages";

// Global vars
let currentPage = 1;
const limit = 6;
let totalPages = 1;

/* =======================================
   LOAD POLICY COVERAGES (GET PAGINATED)
======================================= */
async function loadPolicyCoverages(page = 1) {
  const res = await fetch(`${API}?page=${page}&limit=${limit}`);
  const data = await res.json();

  const tbody = document.querySelector("#policyCoveragesTable");
  tbody.innerHTML = "";

  // Render rows
  data.policy_coverages.forEach(pc => {
    tbody.innerHTML += `
      <tr>
        <td>${pc.policy_id}</td>
        <td>${pc.coverage_id}</td>
        <td>
          <button class="btn btn-sm btn-primary edit-btn" 
                  data-policy="${pc.policy_id}" 
                  data-coverage="${pc.coverage_id}">
            <i class="fas fa-edit"></i>
          </button>

          <button class="btn btn-sm btn-danger delete-btn" 
                  data-policy="${pc.policy_id}" 
                  data-coverage="${pc.coverage_id}">
            <i class="fas fa-trash-alt"></i>
          </button>
        </td>
      </tr>`;
  });

  // Pagination updates
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
  if (currentPage > 1) loadPolicyCoverages(currentPage - 1);
});

document.getElementById("nextPage").addEventListener("click", () => {
  if (currentPage < totalPages) loadPolicyCoverages(currentPage + 1);
});


/* =======================================
   REFRESH BUTTON
======================================= */
const refreshBtn = document.getElementById("refreshBtn");
refreshBtn.addEventListener("click", async () => {
  refreshBtn.classList.add("rotating");
  await loadPolicyCoverages();
  refreshBtn.classList.remove("rotating");
});


/* =======================================
   ADD POLICY COVERAGE (POST)
======================================= */
document.getElementById("policyCoverageForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    policy_id: document.getElementById("policy_id").value,
    coverage_id: document.getElementById("coverage_id").value
  };

  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    bootstrap.Modal.getInstance(document.getElementById("addPolicyCoverageModal")).hide();

    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();

    loadPolicyCoverages();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }

  e.target.reset();
});


/* =======================================
   EDIT POLICY COVERAGE — OPEN MODAL
======================================= */
document.addEventListener("click", async (e) => {
  if (e.target.closest(".edit-btn")) {
    const btn = e.target.closest(".edit-btn");

    const policy_id = btn.dataset.policy;
    const coverage_id = btn.dataset.coverage;

    // Load the existing record
    const res = await fetch(`${API}/${policy_id}/${coverage_id}`);
    const data = await res.json();
    const pc = data.policy_coverage || data;

    // Fill modal
    document.getElementById("edit_id_policy").value = pc.policy_id;
    document.getElementById("edit_id_coverage").value = pc.coverage_id;

    document.getElementById("edit_policy_id").value = pc.policy_id;
    document.getElementById("edit_coverage_id").value = pc.coverage_id;

    const editModal = new bootstrap.Modal(document.getElementById("editModal"));
    editModal.show();
  }
});


/* =======================================
   UPDATE POLICY COVERAGE (PUT)
======================================= */
document.getElementById("editForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const old_policy = document.getElementById("edit_id_policy").value;
  const old_coverage = document.getElementById("edit_id_coverage").value;

  const payload = {
    policy_id: document.getElementById("edit_policy_id").value,
    coverage_id: document.getElementById("edit_coverage_id").value
  };

  const res = await fetch(`${API}/${old_policy}/${old_coverage}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const editModal = bootstrap.Modal.getInstance(document.getElementById("editModal"));
  editModal.hide();

  if (res.ok) {
    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();
    loadPolicyCoverages();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});


/* =======================================
   DELETE POLICY COVERAGE
======================================= */
let policyToDelete = null;
let coverageToDelete = null;

document.addEventListener("click", (e) => {
  const btn = e.target.closest(".delete-btn");

  if (btn) {
    policyToDelete = btn.dataset.policy;
    coverageToDelete = btn.dataset.coverage;

    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    deleteModal.show();
  }
});

document.getElementById("confirmDeleteBtn").addEventListener("click", async () => {
  if (!policyToDelete || !coverageToDelete) return;

  const res = await fetch(`${API}/${policyToDelete}/${coverageToDelete}`, {
    method: "DELETE"
  });

  const deleteModal = bootstrap.Modal.getInstance(document.getElementById("deleteModal"));

  if (res.ok) {
    deleteModal.hide();
    policyToDelete = null;
    coverageToDelete = null;

    loadPolicyCoverages();

    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});


/* INITIAL LOAD */
loadPolicyCoverages();
