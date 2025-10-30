document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll('.chart-tab');
    const sections = document.querySelectorAll('.chart-section');

    // Ocultar todos los gráficos al inicio
    sections.forEach(s => s.style.display = 'none');

    // Mostrar solo el primero por defecto
    const firstSection = document.getElementById('policy-section');
    firstSection.style.display = 'block';

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // quitar "active" de todos los botones y secciones
            tabs.forEach(t => t.classList.remove('active'));
            sections.forEach(s => s.style.display = 'none');

            // activar el seleccionado
            tab.classList.add('active');
            const target = document.getElementById(tab.dataset.target);
            target.style.display = 'block';
            window.dispatchEvent(new Event('resize'))
        });
    });

    // === Cargar datos desde Flask ===
    fetch('/api/dashboard-data')
    .then(response => response.json())
    .then(data => {
        // ====== Gráfico 1: Policy Analytics ======
        const policyCtx = document.getElementById('policyChart').getContext('2d');
        new Chart(policyCtx, {
            type: 'pie',
            data: {
                labels: ['Active', 'Expired', 'Canceled'],
                datasets: [{
                    data: [
                        data.active_policies,
                        data.expired_policies,
                        data.canceled_policies
                    ],
                    backgroundColor: ['#27ae60', '#e67e22', '#c0392b']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Policy Status Distribution'
                    },
                    legend: { position: 'bottom' }
                }
            }
        });

        // ====== Gráfico 2: Customers Analytics ======
        const custCtx = document.getElementById('customerVehicleChart').getContext('2d');
        new Chart(custCtx, {
            type: 'bar',
            data: {
                labels: ['Customers', 'Vehicles'],
                datasets: [{
                    label: 'Count',
                    data: [data.total_customers, data.total_vehicles],
                    backgroundColor: ['#3498db', '#9b59b6']
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } },
                plugins: {
                    title: {
                        display: true,
                        text: 'Customers vs Vehicles'
                    }
                }
            }
        });

        // ====== Gráfico 3: Employment Analytics ======
        const empCtx = document.getElementById('employmentChart').getContext('2d');
        new Chart(empCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Employees added',
                    data: [3, 5, 2, 6, 4, 7], // Ejemplo estático
                    borderColor: '#1e90ff',
                    fill: false,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'New Employees per Month (Example)'
                    }
                }
            }
        });
    })
    .catch(err => console.error('Error fetching chart data:', err));
});
