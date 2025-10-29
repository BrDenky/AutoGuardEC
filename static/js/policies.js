const API = "http://127.0.0.1:5000/api/policies";

async function loadpolicies() {
  const res = await fetch(API);
  const data = await res.json();
  const tbody = document.querySelector("#policiesTable");
  tbody.innerHTML = "";
  data.policies.forEach(p => {
    tbody.innerHTML += `
      <tr>
        <td>${p.policy_id}</td>
        <td>${p.customer_id}</td>
        <td>${p.vehicle_id}</td>
        <td>${p.agent_id}</td>
        <td>${p.start_date}</td>
        <td>${p.end_date}</td>
        <td>${p.status}</td>
      </tr>`;
  });
}

document.getElementById("policyForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    customer_id: document.getElementById("customer_id").value,
    vehicle_id: document.getElementById("vehicle_id").value,
    agent_id: document.getElementById("agent_id").value,
    start_date: document.getElementById("start_date").value,
    end_date: document.getElementById("end_date").value,
    status: document.getElementById("status").value
  };
  await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  loadpolicies();
});

loadpolicies();
