// ================================================
// POLICY QUICK VIEW (OPEN FROM POLICIES TABLE)
// ================================================
document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".policy-qv-btn");
  if (!btn) return;

  const policyId = btn.dataset.id;
  openPolicyQuickView(policyId);
});

async function openPolicyQuickView(policyId) {
  const spinner = document.getElementById("policyLoadingSpinner");
  const content = document.getElementById("policyQuickViewContent");

  spinner.style.display = "block";
  content.style.display = "none";

  const modal = new bootstrap.Modal(
    document.getElementById("policyQuickViewModal")
  );
  modal.show();

  try {
    const res = await fetch(`http://127.0.0.1:5000/api/policies/${policyId}`);
    const data = await res.json();

    // Fill main info
    document.getElementById("qv_policy_title").textContent =
      `Policy #${data.policy_id} (${data.status})`;

    document.getElementById("qv_policy_id").textContent = data.policy_id;
    document.getElementById("qv_policy_status").textContent = data.status;
    document.getElementById("qv_policy_start").textContent = data.start_date;
    document.getElementById("qv_policy_end").textContent = data.end_date;

    // Linked entities
    document.getElementById("qv_policy_customer").textContent =
      `${data.customer.name} (ID: ${data.customer.customer_id})`;

    document.getElementById("qv_policy_vehicle").textContent =
      `${data.vehicle.brand} ${data.vehicle.model} - ${data.vehicle.license_plate}`;

    document.getElementById("qv_policy_agent").textContent =
      `${data.agent.name} (ID: ${data.agent.agent_id})`;

    // Profile button
    document.getElementById("policyFullProfileBtn").href =
      `/policies/${policyId}/profile`;

    // Coverages
    const cList = document.getElementById("qv_policy_coverages");
    cList.innerHTML = "";
    if (data.coverages.length > 0) {
      data.coverages.forEach(c => {
        cList.innerHTML += `
          <li class="list-group-item d-flex justify-content-between">
            <strong>${c.name}</strong>
            <span class="text-muted">${c.type || ""}</span>
          </li>
        `;
      });
    } else {
      cList.innerHTML = `<li class="list-group-item text-muted">No coverages.</li>`;
    }

    // Claims
    const clList = document.getElementById("qv_policy_claims");
    clList.innerHTML = "";
    if (data.claims.length > 0) {
      data.claims.forEach(cl => {
        clList.innerHTML += `
          <li class="list-group-item">
            Claim #${cl.claim_id} — ${cl.status}
          </li>
        `;
      });
    } else {
      clList.innerHTML = `<li class="list-group-item text-muted">No claims.</li>`;
    }

    // Premium Payments
    const pList = document.getElementById("qv_policy_payments");
    pList.innerHTML = "";
    if (data.premium_payments.length > 0) {
      data.premium_payments.forEach(p => {
        pList.innerHTML += `
          <li class="list-group-item">
            Payment #${p.payment_id} — ${p.amount}
          </li>
        `;
      });
    } else {
      pList.innerHTML = `<li class="list-group-item text-muted">No payments.</li>`;
    }

    spinner.style.display = "none";
    content.style.display = "block";

  } catch (err) {
    console.error("Error loading policy:", err);
    spinner.innerHTML = `<p class="text-danger">Error loading policy data.</p>`;
  }
}
