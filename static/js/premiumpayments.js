const API = "http://127.0.0.1:5000/api/premium_payments";

// Global vars
let currentPage = 1;
const limit = 6;
let totalPages = 1;

/* ================================
   LOAD PAYMENTS (GET PAGINATED)
================================ */
async function loadPayments(page = 1) {
  const res = await fetch(`${API}?page=${page}&limit=${limit}`);
  const data = await res.json();

  const tbody = document.querySelector("#paymentsTable");
  tbody.innerHTML = "";

  // Render rows
  data.premium_payments.forEach(p => {
    tbody.innerHTML += `
      <tr>
        <td>${p.payment_id}</td>
        <td>
          <button class="btn btn-link p-0 policy-qv-btn" data-id="${p.policy_id}">
            ${p.policy_id}
          </button>
        </td>
        <td>${p.payment_date}</td>
        <td>$${p.amount}</td>
        <td>
          <button class="btn btn-sm btn-primary edit-btn" data-id="${p.payment_id}">
            <i class="fas fa-edit"></i>
          </button>

          <button class="btn btn-sm btn-danger delete-btn" data-id="${p.payment_id}">
            <i class="fas fa-trash-alt"></i>
          </button>
        </td>
      </tr>`;
  });

  // Pagination update
  currentPage = data.current_page;
  totalPages = data.total_pages;

  document.getElementById("pageInfo").textContent =
    `Page ${currentPage} of ${totalPages}`;

  document.getElementById("prevPage").disabled = !data.has_prev;
  document.getElementById("nextPage").disabled = !data.has_next;
}


/* ================================
   PAGINATION BUTTONS
================================ */
document.getElementById("prevPage").addEventListener("click", () => {
  if (currentPage > 1) loadPayments(currentPage - 1);
});

document.getElementById("nextPage").addEventListener("click", () => {
  if (currentPage < totalPages) loadPayments(currentPage + 1);
});


/* ================================
   REFRESH BUTTON
================================ */
const refreshBtn = document.getElementById("refreshBtn");
refreshBtn.addEventListener("click", async () => {
  refreshBtn.classList.add("rotating");
  await loadPayments();
  refreshBtn.classList.remove("rotating");
});


/* ================================
   ADD PAYMENT (POST)
================================ */
document.getElementById("paymentForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    policy_id: document.getElementById("policy_id").value,
    payment_date: document.getElementById("payment_date").value,
    amount: document.getElementById("amount").value
  };

  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    bootstrap.Modal.getInstance(document.getElementById("addPaymentModal")).hide();
    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();
    loadPayments();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }

  e.target.reset();
});


/* ================================
   EDIT PAYMENT (FILL MODAL)
================================ */
document.addEventListener("click", async (e) => {
  if (e.target.closest(".edit-btn")) {
    const id = e.target.closest(".edit-btn").dataset.id;

    // Fetch payment by ID
    const res = await fetch(`${API}/${id}`);
    const data = await res.json();
    const p = data.premium_payment || data;

    document.getElementById("edit_id").value = p.payment_id;
    document.getElementById("edit_policy_id").value = p.policy_id;
    document.getElementById("edit_payment_date").value = p.payment_date;
    document.getElementById("edit_amount").value = p.amount;

    const editModal = new bootstrap.Modal(document.getElementById("editModal"));
    editModal.show();
  }
});


/* ================================
   UPDATE PAYMENT (PUT)
================================ */
document.getElementById("editForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = document.getElementById("edit_id").value;

  const payload = {
    policy_id: document.getElementById("edit_policy_id").value,
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
    loadPayments();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});


/* ================================
   DELETE PAYMENT (MODAL CONFIRM)
================================ */
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
    loadPayments();

    const toast = new bootstrap.Toast(document.getElementById("toastSuccess"));
    toast.show();
  } else {
    const toast = new bootstrap.Toast(document.getElementById("toastError"));
    toast.show();
  }
});


/* INITIAL LOAD */
loadPayments();
