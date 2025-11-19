// ================================================
// AGENT QUICK VIEW (OPEN FROM AGENTS TABLE)
// ================================================
document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".agent-qv-btn");
  if (!btn) return;

  const agentId = btn.dataset.id;
  openAgentQuickView(agentId);
});

async function openAgentQuickView(agentId) {
  const spinner = document.getElementById("agentLoadingSpinner");
  const content = document.getElementById("agentQuickViewContent");

  // Reset states
  spinner.style.display = "block";
  content.style.display = "none";

  // Open modal
  const modal = new bootstrap.Modal(
    document.getElementById("agentQuickViewModal")
  );
  modal.show();

  try {
    // Fetch agent
    const res = await fetch(`http://127.0.0.1:5000/api/agents/${agentId}`);
    const data = await res.json();

    // Fill modal fields
    document.getElementById("qv_agent_name").textContent = data.name || "Unknown";
    document.getElementById("qv_agent_id").textContent = data.agent_id;
    document.getElementById("qv_agent_email").textContent = data.email || "N/A";
    document.getElementById("qv_agent_phone").textContent = data.phone || "N/A";

    // Full profile link
    document.getElementById("agentFullProfileBtn").href =
      `/agents/${agentId}/profile`;

    // Fill policies list
    const pList = document.getElementById("qv_agent_policies");
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
        <li class="list-group-item text-muted">No policies assigned.</li>
      `;
    }

    spinner.style.display = "none";
    content.style.display = "block";

  } catch (err) {
    console.error("Error loading agent:", err);
    spinner.innerHTML = `<p class="text-danger">Error loading agent data.</p>`;
  }
}
