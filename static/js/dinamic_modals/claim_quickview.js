// ================================================
// CLAIM QUICK VIEW (OPEN FROM CLAIMS TABLE)
// ================================================
document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".claim-qv-btn");
  if (!btn) return;

  const claimId = btn.dataset.id;
  openClaimQuickView(claimId);
});

async function openClaimQuickView(claimId) {
  const spinner = document.getElementById("claimLoadingSpinner");
  const content = document.getElementById("claimQuickViewContent");

  spinner.style.display = "block";
  content.style.display = "none";

  const modal = new bootstrap.Modal(
    document.getElementById("claimQuickViewModal")
  );
  modal.show();

  try {
    const res = await fetch(`http://127.0.0.1:5000/api/claims/${claimId}`);
    const data = await res.json();

    // Title
    document.getElementById("qv_claim_title").textContent =
      `Claim #${data.claim_id} (${data.status})`;

    // Main fields
    document.getElementById("qv_claim_id").textContent = data.claim_id;
    document.getElementById("qv_claim_status").textContent = data.status;
    document.getElementById("qv_claim_date").textContent = data.claim_date;
    document.getElementById("qv_claim_policy").textContent = data.policy_id;
    document.getElementById("qv_claim_description").textContent = data.description;

    // Profile link
    document.getElementById("claimFullProfileBtn").href =
      `/claims/${claimId}/profile`;

    // Claim Payments
    const cpList = document.getElementById("qv_claim_payments");
    cpList.innerHTML = "";

    if (data.claim_payments && data.claim_payments.length > 0) {
      data.claim_payments.forEach(p => {
        cpList.innerHTML += `
          <li class="list-group-item d-flex justify-content-between">
            <strong>Payment #${p.claim_payment_id}</strong>
            <span class="text-muted">
              ${p.payment_date} — $${p.amount}
            </span>
          </li>
        `;
      });
    } else {
      cpList.innerHTML =
        `<li class="list-group-item text-muted">No claim payments.</li>`;
    }

    spinner.style.display = "none";
    content.style.display = "block";

  } catch (err) {
    console.error("Error loading claim:", err);
    spinner.innerHTML = `<p class="text-danger">Error loading claim data.</p>`;
  }
}
