const API = "http://127.0.0.1:5000/api/claim_payments";

// Global vars
let currentPage = 1;
const limit = 6;
let totalPages = 1;

/* =======================================
   LOAD CLAIM PAYMENTS (GET PAGINATED)
======================================= */
async function loadClaimPayments(page = 1) {
  const res = await fetch(`${API}?page=${page}&limit=${limit}`);
  const data = await res.json();

  const tbody = document.querySelector("#claimPaymentsTable");
  tbody.innerHTML = "";

  // Render rows
  data.claim_payments.forEach(p => {
    tbody.innerHTML += `
      <tr>
        <td>${p.claim_payment_id}</td>
        <td>${p.claim_id}</td>
        <td>${p.payment_date}</td>
        <td>$${p.amount}</td>
        <td>
          <button class="btn btn-sm btn-primary edit-btn" data-id="${p.claim_payment_id}">
            <i class="fas fa-edit"></i>
          </button>

          <button class="btn btn-sm btn-danger delete-btn" data-id="${p.claim_payment_id}">
            <i class="fas fa-trash-alt"></i>
          </button>
        </td>
      </tr>`;
  });

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
  if (currentPage > 1) loadClaimPayments(currentPage - 1);
});

document.getElementById("nextPage").addEventListener("click", () => {
  if (currentPage < totalPages) loadClaimPayments(currentPage + 1);
});


/* =======================================
   REFRESH BUTTON
======================================= */
const refreshBtn = document.getElementById("refreshBtn");
refreshBtn.addEventListener("click", async () => {
  refreshBtn.classList.add("rotating");
  await loadClaimPayments();
  refreshBtn.classList.remove("rotating");
});


/* =======================================
   ADD CLAIM PAYMENT (POST)
======================================= */
document.getElementById("claimPaymentForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    claim_id: document.getElementById("claim_id").value,
    payment_date: document.getElementById("payment_date").value,
    amount: document.getElementById("amount").value
  };

  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    bootstrap.Modal.getInstance(document.getElementById("addClaimPaymentModal")).hide();

    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();

    loadClaimPayments();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }

  e.target.reset();
});


/* =======================================
   EDIT CLAIM PAYMENT — OPEN MODAL
======================================= */
document.addEventListener("click", async (e) => {
  if (e.target.closest(".edit-btn")) {
    const id = e.target.closest(".edit-btn").dataset.id;

    const res = await fetch(`${API}/${id}`);
    const data = await res.json();
    const p = data.claim_payment || data;

    // Fill modal fields
    document.getElementById("edit_id").value = p.claim_payment_id;
    document.getElementById("edit_claim_id").value = p.claim_id;
    document.getElementById("edit_payment_date").value = p.payment_date;
    document.getElementById("edit_amount").value = p.amount;

    // Show modal
    const editModal = new bootstrap.Modal(document.getElementById("editModal"));
    editModal.show();
  }
});


/* =======================================
   UPDATE CLAIM PAYMENT (PUT)
======================================= */
document.getElementById("editForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = document.getElementById("edit_id").value;

  const payload = {
    claim_id: document.getElementById("edit_claim_id").value,
    payment_date: document.getElementById("edit_payment_date").value,
    amount: document.getElementById("edit_amount").value
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
    loadClaimPayments();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});


/* =======================================
   DELETE CLAIM PAYMENT (MODAL CONFIRMATION)
======================================= */
let paymentToDelete = null;

document.addEventListener("click", (e) => {
  const btn = e.target.closest(".delete-btn");
  if (btn) {
    paymentToDelete = btn.dataset.id;
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    deleteModal.show();
  }
});

document.getElementById("confirmDeleteBtn").addEventListener("click", async () => {
  if (!paymentToDelete) return;

  const res = await fetch(`${API}/${paymentToDelete}`, {
    method: "DELETE"
  });

  const deleteModal = bootstrap.Modal.getInstance(document.getElementById("deleteModal"));

  if (res.ok) {
    deleteModal.hide();
    paymentToDelete = null;
    loadClaimPayments();

    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});


/* INITIAL LOAD */
loadClaimPayments();
