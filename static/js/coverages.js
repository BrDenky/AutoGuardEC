const API = "http://127.0.0.1:5000/api/coverages";

// Variables globales
let currentPage = 1;
const limit = 6;
let totalPages = 1;

/* Load Coverages - GET (Paginated) */
async function loadCoverages(page = 1) {
  const res = await fetch(`${API}?page=${page}&limit=${limit}`);
  const data = await res.json();

  const tbody = document.querySelector("#coveragesTable");
  tbody.innerHTML = "";

  data.coverages.forEach(c => {
    tbody.innerHTML += `
      <tr>
        <td>${c.coverage_id}</td>
        <td>${c.name}</td>
        <td>${c.description}</td>
        <td>
          <button class="btn btn-sm btn-primary edit-btn" data-id="${c.coverage_id}">
            <i class="fas fa-edit"></i>
          </button>
          <button class="btn btn-sm btn-danger delete-btn" data-id="${c.coverage_id}">
            <i class="fas fa-trash-alt"></i>
          </button>
        </td>
      </tr>`;
  });
}

/* Initial Load */
loadCoverages();

/* Refresh */
document.getElementById("refreshBtn").addEventListener("click", async () => {
  await loadCoverages();
});

/* --- Add Coverage --- */
document.getElementById("coverageForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    name: document.getElementById("name").value,
    description: document.getElementById("description").value
  };

  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    const addModal = bootstrap.Modal.getInstance(document.getElementById("addCoverageModal"));
    addModal.hide();
    loadCoverages();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }

  e.target.reset();
});

/* --- Edit Coverage --- */
document.addEventListener("click", async (e) => {
  if (e.target.closest(".edit-btn")) {
    const id = e.target.closest(".edit-btn").dataset.id;
    const res = await fetch(`${API}/${id}`);
    const data = await res.json();
    const c = data.coverage || data;

    document.getElementById("edit_id").value = c.coverage_id;
    document.getElementById("edit_name").value = c.name;
    document.getElementById("edit_description").value = c.description;

    const editModal = new bootstrap.Modal(document.getElementById("editModal"));
    editModal.show();
  }
});

document.getElementById("editForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = document.getElementById("edit_id").value;

  const payload = {
    name: document.getElementById("edit_name").value,
    description: document.getElementById("edit_description").value
  };

  await fetch(`${API}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const editModal = bootstrap.Modal.getInstance(document.getElementById("editModal"));
  editModal.hide();
  loadCoverages();
});

/* --- Delete Coverage --- */
let coverageToDelete = null;

document.addEventListener("click", (e) => {
  const del = e.target.closest(".delete-btn");
  if (del) {
    coverageToDelete = del.dataset.id;
    const modal = new bootstrap.Modal(document.getElementById("deleteModal"));
    modal.show();
  }
});

document.getElementById("confirmDeleteBtn").addEventListener("click", async () => {
  if (!coverageToDelete) return;

  const res = await fetch(`${API}/${coverageToDelete}`, { method: "DELETE" });
  const modal = bootstrap.Modal.getInstance(document.getElementById("deleteModal"));

  if (res.ok) {
    modal.hide();
    loadCoverages();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});
