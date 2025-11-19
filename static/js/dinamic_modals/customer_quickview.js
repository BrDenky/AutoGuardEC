// ================================================
// CUSTOMER QUICK VIEW (OPEN FROM VEHICLES TABLE)
// ================================================
document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".customer-qv-btn");
  if (!btn) return;

  const customerId = btn.dataset.id;
  openCustomerQuickView(customerId);
});

async function openCustomerQuickView(customerId) {
  const spinner = document.getElementById("customerLoadingSpinner");
  const content = document.getElementById("customerQuickViewContent");

  // Reset states
  spinner.style.display = "block";
  content.style.display = "none";

  // Open modal
  const modal = new bootstrap.Modal(document.getElementById("customerQuickViewModal"));
  modal.show();

  try {
    // Fetch customer
    const res = await fetch(`http://127.0.0.1:5000/api/customers/${customerId}`);
    const data = await res.json();

    // Fill modal fields
    document.getElementById("qv_customer_name").textContent = data.name || "Unknown";
    document.getElementById("qv_customer_id").textContent = data.customer_id || data.id;
    document.getElementById("qv_customer_email").textContent = data.email || "N/A";
    document.getElementById("qv_customer_phone").textContent = data.phone || "N/A";
    document.getElementById("qv_customer_address").textContent = data.address || "N/A";

    // Full profile link
    document.getElementById("customerFullProfileBtn").href =
      `/customers/${customerId}/profile`;

    // Fill vehicles list
    const vList = document.getElementById("qv_customer_vehicles");
    vList.innerHTML = "";

    if (data.vehicles && data.vehicles.length > 0) {
      data.vehicles.forEach(v => {
        vList.innerHTML += `
          <li class="list-group-item d-flex justify-content-between">
            <strong>${v.brand} ${v.model}</strong>
            <span class="text-muted">${v.license_plate}</span>
          </li>
        `;
      });
    } else {
      vList.innerHTML = `
        <li class="list-group-item text-muted">No vehicles found.</li>
      `;
    }

    // Show content and hide spinner
    spinner.style.display = "none";
    content.style.display = "block";

  } catch (err) {
    console.error("Error loading customer:", err);
    spinner.innerHTML = `<p class="text-danger">Error loading customer data.</p>`;
  }
}
