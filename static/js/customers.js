const API = "http://127.0.0.1:5000/api/customers";

async function loadCustomers() {
  const res = await fetch(API);
  const data = await res.json();
  const tbody = document.querySelector("#customersTable");
  tbody.innerHTML = "";
  data.customers.forEach(c => {
    tbody.innerHTML += `
      <tr>
        <td>${c.customer_id}</td>
        <td>${c.first_name}</td>
        <td>${c.last_name}</td>
        <td>${c.address}</td>
        <td>${c.phone}</td>
        <td>${c.email}</td>
      </tr>`;
  });
}

document.getElementById("customerForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    first_name: document.getElementById("first_name").value,
    last_name: document.getElementById("last_name").value,
    address: document.getElementById("address").value,
    phone: document.getElementById("phone").value,
    email: document.getElementById("email").value
  };
  await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  loadCustomers();
});

loadCustomers();
