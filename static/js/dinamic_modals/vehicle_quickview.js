// ================================================
// VEHICLE QUICK VIEW (OPEN FROM VEHICLES TABLE)
// ================================================
document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".vehicle-qv-btn");
  if (!btn) return;

  const vehicleId = btn.dataset.id;
  openVehicleQuickView(vehicleId);
});

async function openVehicleQuickView(vehicleId) {
  const spinner = document.getElementById("vehicleLoadingSpinner");
  const content = document.getElementById("vehicleQuickViewContent");

  // Reset states
  spinner.style.display = "block";
  content.style.display = "none";

  // Open modal
  const modal = new bootstrap.Modal(
    document.getElementById("vehicleQuickViewModal")
  );
  modal.show();

  try {
    // Fetch vehicle
    const res = await fetch(`http://127.0.0.1:5000/api/vehicles/${vehicleId}`);
    const data = await res.json();

    // === Fill modal fields ===

    // Title: Brand + Model + Year
    document.getElementById("qv_vehicle_title").textContent =
      `${data.brand || ""} ${data.model || ""} (${data.year || "N/A"})`;

    document.getElementById("qv_vehicle_id").textContent = data.vehicle_id;
    document.getElementById("qv_vehicle_brand").textContent = data.brand || "N/A";
    document.getElementById("qv_vehicle_model").textContent = data.model || "N/A";
    document.getElementById("qv_vehicle_year").textContent = data.year || "N/A";
    document.getElementById("qv_vehicle_plate").textContent = data.license_plate || "N/A";
    document.getElementById("qv_vehicle_customer_id").textContent = data.customer_id || "N/A";

    // Full profile link
    document.getElementById("vehicleFullProfileBtn").href =
      `/vehicles/${vehicleId}/profile`;

    // === Fill policies list ===
    const pList = document.getElementById("qv_vehicle_policies");
    pList.innerHTML = "";

    if (data.policies && data.policies.length > 0) {
      data.policies.forEach(p => {
        pList.innerHTML += `
          <li class="list-group-item d-flex justify-content-between">
            <strong>Policy #${p.policy_id}</strong>
            <span class="text-muted">${p.status || "N/A"}</span>
          </li>
        `;
      });
    } else {
      pList.innerHTML = `
        <li class="list-group-item text-muted">No policies found.</li>
      `;
    }

    // Show content and hide spinner
    spinner.style.display = "none";
    content.style.display = "block";

  } catch (err) {
    console.error("Error loading vehicle:", err);
    spinner.innerHTML = `<p class="text-danger">Error loading vehicle data.</p>`;
  }
}
