const API = "http://127.0.0.1:5000/api/vehicles";

// Variables globales
let currentPage = 1;
const limit = 6;
let totalPages = 1;
let currentSearchQuery = ''; // Track current search query

/* Load Vehicles - GET (Paginated) */
async function loadVehicles(page = 1, searchQuery = '') {
  let url = `${API}?page=${page}&limit=${limit}`;

  // If there's a search query, use the search endpoint
  if (searchQuery.trim()) {
    url = `${API}/search?q=${encodeURIComponent(searchQuery)}&page=${page}&limit=${limit}`;
  }

  const res = await fetch(url);
  const data = await res.json();

  const tbody = document.querySelector("#vehiclesTable");
  tbody.innerHTML = "";

  // Render table rows
  data.vehicles.forEach(v => {
    tbody.innerHTML += `
      <tr>
        <td>${v.vehicle_id}</td>
        <td>
          <button class="btn btn-link p-0 customer-qv-btn" data-id="${v.customer_id}">
            ${v.customer_id}
          </button>
        </td>
        <td>${v.brand}</td>
        <td>${v.model}</td>
        <td>${v.year || 'N/A'}</td>
        <td>${v.license_plate}</td>
        <td>
          <button class="btn btn-sm btn-primary edit-btn" data-id="${v.vehicle_id}">
            <i class="fas fa-edit"></i>
          </button>
          <button class="btn btn-sm btn-danger delete-btn" data-id="${v.vehicle_id}">
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
  if (currentPage > 1) loadVehicles(currentPage - 1, currentSearchQuery);
});

document.getElementById("nextPage").addEventListener("click", () => {
  if (currentPage < totalPages) loadVehicles(currentPage + 1, currentSearchQuery);
});

/* Initial load */
loadVehicles();

/* Refresh vehicles list when clicking the "Refresh" button */
const refreshBtn = document.getElementById("refreshBtn");
refreshBtn.addEventListener("click", async () => {
  refreshBtn.classList.add("rotating");
  await loadVehicles(currentPage);
  refreshBtn.classList.remove("rotating");
});

/* --- Add Vehicle Logic --- */
document.getElementById("vehicleForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    customer_id: parseInt(document.getElementById("customer_id").value),
    brand: document.getElementById("brand").value,
    model: document.getElementById("model").value,
    year: parseInt(document.getElementById("year").value) || null,
    license_plate: document.getElementById("license_plate").value
  };

  await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  // Close modal
  const addModal = bootstrap.Modal.getInstance(document.getElementById("addVehicleModal"));
  addModal.hide();

  // Reset form
  document.getElementById("vehicleForm").reset();

  // Refresh table
  loadVehicles(currentPage);
});

/* --- Edit Vehicle Logic --- */

// Detect clicks on Edit buttons
document.addEventListener("click", async (e) => {
  if (e.target.closest(".edit-btn")) {
    const id = e.target.closest(".edit-btn").dataset.id;

    // Fetch vehicle data by ID
    const res = await fetch(`${API}/${id}`);
    const data = await res.json();
    const vehicle = data.vehicle || data;

    // Fill modal fields
    document.getElementById("edit_id").value = vehicle.vehicle_id;
    document.getElementById("edit_customer_id").value = vehicle.customer_id;
    document.getElementById("edit_brand").value = vehicle.brand;
    document.getElementById("edit_model").value = vehicle.model;
    document.getElementById("edit_year").value = vehicle.year || '';
    document.getElementById("edit_license_plate").value = vehicle.license_plate;

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
    brand: document.getElementById("edit_brand").value,
    model: document.getElementById("edit_model").value,
    year: parseInt(document.getElementById("edit_year").value) || null,
    license_plate: document.getElementById("edit_license_plate").value
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
  loadVehicles(currentPage);
});

/* --- Delete Vehicle Logic --- */
let vehicleToDelete = null;

// Detect clicks on Delete buttons
document.addEventListener("click", (e) => {
  const deleteBtn = e.target.closest(".delete-btn");
  if (deleteBtn) {
    vehicleToDelete = deleteBtn.dataset.id;
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    deleteModal.show();
  }
});

// Confirm deletion when user clicks "Delete" in modal
document.getElementById("confirmDeleteBtn").addEventListener("click", async () => {
  if (!vehicleToDelete) return;

  const res = await fetch(`${API}/${vehicleToDelete}`, { method: "DELETE" });
  const deleteModal = bootstrap.Modal.getInstance(document.getElementById("deleteModal"));

  if (res.ok) {
    deleteModal.hide();
    vehicleToDelete = null;
    loadVehicles(currentPage);

    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});

/* Search functionality with debouncing */
const searchInput = document.getElementById("vehicleSearchInput");
let searchDebounceTimer;

searchInput.addEventListener("input", (e) => {
  clearTimeout(searchDebounceTimer);

  searchDebounceTimer = setTimeout(() => {
    currentSearchQuery = e.target.value.trim();
    currentPage = 1; // Reset to first page on new search
    loadVehicles(1, currentSearchQuery);
  }, 300); // 300ms debounce delay
});