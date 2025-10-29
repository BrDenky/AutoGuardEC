const API = "http://127.0.0.1:5000/api/vehicles";

async function loadvehicles() {
  const res = await fetch(API);
  const data = await res.json();
  const tbody = document.querySelector("#vehiclesTable");
  tbody.innerHTML = "";
  data.vehicles.forEach(v => {
    tbody.innerHTML += `
      <tr>
        <td>${v.vehicle_id}</td>
        <td>${v.customer_id}</td>
        <td>${v.brand}</td>
        <td>${v.model}</td>
        <td>${v.year}</td>
        <td>${v.license_plate}</td>
      </tr>`;
  });
}

document.getElementById("vehicleForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    customer_id: document.getElementById("customer_id").value,
    brand: document.getElementById("brand").value,
    model: document.getElementById("model").value,
    year: document.getElementById("year").value,
    license_plate: document.getElementById("license_plate").value
  };
  await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  loadvehicles();
});

loadvehicles();
