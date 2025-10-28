# ============================================================
#  CarInsuranceDB Data Generator - Ecuador Version
#  Generates coherent, realistic SQL INSERT statements
#  Author: ChatGPT (GPT-5)
# ============================================================

import random
from datetime import datetime, timedelta, date

# -----------------------------------------------
#  Try importing Faker for realistic names
# -----------------------------------------------
try:
    from faker import Faker
    fake = Faker("es_ES")
    Faker_available = True
    fake.seed_instance(42)
except:
    Faker_available = False

# ============================================================
#  CONFIGURATION
# ============================================================
NUM_CUSTOMERS = 350
NUM_VEHICLES = 750
NUM_AGENTS = 25
NUM_POLICIES = 500
NUM_POLICY_COVERAGE = 1000
NUM_CLAIMS_APPROX = 280

MIN_COV_PER_POLICY = 2
MAX_COV_PER_POLICY = 3
MIN_PAYMENTS_PER_POLICY = 2
MAX_PAYMENTS_PER_POLICY = 4
MIN_CLAIM_PAYMENTS = 0
MAX_CLAIM_PAYMENTS = 2

# ============================================================
#  REFERENCE DATA
# ============================================================
COVERAGES = [
    ("Responsabilidad civil", "Cubre daños a terceros ocasionados por el vehículo asegurado."),
    ("Daños a terceros", "Cubre los gastos de reparación o compensación a terceros afectados."),
    ("Robo total", "Protege al propietario en caso de pérdida total por robo."),
    ("Pérdida total", "Aplica cuando los daños superan el 75% del valor del vehículo."),
    ("Asistencia en carretera", "Incluye grúa, cambio de llantas, y ayuda por averías.")
]

PROVINCES = {
    "Pichincha": ["Quito"],
    "Guayas": ["Guayaquil"],
    "Azuay": ["Cuenca"],
    "Tungurahua": ["Ambato"],
    "Loja": ["Loja"],
    "Manabí": ["Manta", "Portoviejo"],
    "Imbabura": ["Ibarra"],
    "Esmeraldas": ["Esmeraldas"],
    "Chimborazo": ["Riobamba"]
}

PROVINCE_WEIGHTS = {
    "Pichincha": 35, "Guayas": 25, "Azuay": 10, "Tungurahua": 8,
    "Loja": 5, "Manabí": 5, "Imbabura": 4, "Esmeraldas": 4, "Chimborazo": 4
}

PLATE_PREFIX = {
    "Pichincha": "P", "Guayas": "G", "Azuay": "A", "Tungurahua": "T",
    "Loja": "L", "Manabí": "M", "Imbabura": "I", "Esmeraldas": "E", "Chimborazo": "H"
}

STREET_TYPES = ["Av.", "Calle", "Avenida", "Pasaje"]
STREET_NAMES = [
    "Amazonas", "10 de Agosto", "9 de Octubre", "Shyris", "Patria", "Bolívar", 
    "Olmedo", "Gran Colombia", "Eloy Alfaro", "Simón Bolívar", "La República"
]
SECTORS = [
    "La Carolina", "Centro", "La Floresta", "El Bosque", "Santa Rosa",
    "Bellavista", "Carcelén", "San Juan", "San Blas", "Los Chillos"
]

BRANDS = [
    "Chevrolet", "Toyota", "Hyundai", "Kia", "Nissan", "Mazda", "Ford",
    "Volkswagen", "Suzuki", "Renault", "Honda", "Great Wall", "Chery"
]

POLICY_STATUSES = ["active", "expired", "canceled", "arrears"]
CLAIM_STATUSES = ["open", "closed", "in review"]




# Claim Function description
def fake_claim_description():
    tipos = [
        "colisión leve", "colisión frontal", "choque por alcance",
        "daños por inundación", "accidente con motocicleta",
        "robo de vehículo", "robo de accesorios", "daños en parabrisas",
        "incendio parcial", "caída de objeto sobre el vehículo",
        "vandalismo", "deslizamiento de tierra", "accidente en autopista"
    ]
    causas = [
        "por imprudencia del conductor", "por fallas mecánicas",
        "debido a condiciones climáticas", "provocado por un tercero",
        "durante el estacionamiento", "mientras estaba en circulación",
        "ocurrido durante la noche", "durante una tormenta"
    ]
    lugares = [
        "en la Av. 10 de Agosto", "cerca del Parque La Carolina",
        "en la vía a Guayllabamba", "en el centro de Guayaquil",
        "en la Panamericana Sur", "en la Av. de las Américas",
        "en la Av. Loja", "en el redondel de Cuenca"
    ]
    return f"Reclamo por {random.choice(tipos)} {random.choice(causas)} {random.choice(lugares)}."




# ============================================================
#  HELPER FUNCTIONS
# ============================================================
def weighted_choice(d):
    return random.choices(list(d.keys()), weights=list(d.values()), k=1)[0]

def rand_date(start_year=2020, end_year=2025):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_plate(province):
    prefix = PLATE_PREFIX.get(province, "P")
    letters = "".join(random.choices("BCDFGHJKLMNPQRSTVWXYZ", k=2))
    numbers = random.randint(1000, 9999)
    return f"{prefix}{letters}-{numbers}"

def address(city, province):
    st = random.choice(STREET_TYPES)
    sn = random.choice(STREET_NAMES)
    sec = random.choice(SECTORS)
    num = f"N{random.randint(1,50)}-{random.randint(100,999)}"
    return f"{st} {sn} {num}, Sector {sec}, {city}, {province}"

def sql_str(s):
    return str(s).replace("'", "''")

# ============================================================
#  GENERATION
# ============================================================
customers, agents, vehicles, policies = [], [], [], []
policy_coverages, premium_payments, claims, claim_payments = [], [], [], []

# Customers
for i in range(1, NUM_CUSTOMERS + 1):
    province = weighted_choice(PROVINCE_WEIGHTS)
    city = random.choice(PROVINCES[province])
    if Faker_available:
        first, last = fake.first_name(), fake.last_name()
    else:
        first, last = f"Nombre{i}", f"Apellido{i}"
    addr = address(city, province)
    phone = f"+593-{random.randint(900000000,999999999)}"
    email = f"{first.lower()}.{last.lower()}@gmail.com"
    customers.append((i, first, last, addr, phone, email, city, province))

# Agents
for i in range(1, NUM_AGENTS + 1):
    province = weighted_choice(PROVINCE_WEIGHTS)
    city = random.choice(PROVINCES[province])
    name = fake.name() if Faker_available else f"Agente {i}"
    phone = f"+593-{random.randint(800000000,899999999)}"
    email = f"agente{i}@aseguradora.ec"
    agents.append((i, name, phone, email, city, province))

# Vehicles
vid = 1
for c in customers:
    num_vehicles = random.randint(1, 3)
    for _ in range(num_vehicles):
        if vid > NUM_VEHICLES: break
        brand = random.choice(BRANDS)
        model = f"Modelo{random.randint(1,100)}"
        year = random.randint(2005, 2025)
        plate = generate_plate(c[7])
        vehicles.append((vid, c[0], brand, model, year, plate))
        vid += 1
    if vid > NUM_VEHICLES: break

# Policies
for i in range(1, NUM_POLICIES + 1):
    cust = random.choice(customers)
    cust_id = cust[0]
    agent = random.choice([a for a in agents if a[5] == cust[7]] or agents)
    vehicle = random.choice([v for v in vehicles if v[1] == cust_id])
    start = rand_date()
    end = start + timedelta(days=random.randint(180, 720))
    status = random.choice(POLICY_STATUSES)
    policies.append((i, cust_id, vehicle[0], agent[0], start, end, status))

# PolicyCoverage
for p in policies:
    covs = random.sample(range(1, len(COVERAGES)+1), random.randint(MIN_COV_PER_POLICY, MAX_COV_PER_POLICY))
    for c in covs:
        policy_coverages.append((p[0], c))

# PremiumPayments
pay_id = 1
for p in policies:
    n = random.randint(MIN_PAYMENTS_PER_POLICY, MAX_PAYMENTS_PER_POLICY)
    for _ in range(n):
        d = p[4] + timedelta(days=random.randint(0, (p[5]-p[4]).days))
        amt = round(random.uniform(80, 1200), 2)
        premium_payments.append((pay_id, p[0], d, amt))
        pay_id += 1

# Claims
claim_id = 1
for p in random.sample(policies, int(NUM_POLICIES * 0.45)):
    n = random.choice([1, 2])
    for _ in range(n):
        d = p[4] + timedelta(days=random.randint(0, 365))
        desc = fake_claim_description()
        status = random.choice(CLAIM_STATUSES)
        claims.append((claim_id, p[0], d, desc, status))
        claim_id += 1

# ClaimPayments
cp_id = 1
for c in claims:
    for _ in range(random.randint(MIN_CLAIM_PAYMENTS, MAX_CLAIM_PAYMENTS)):
        d = c[2] + timedelta(days=random.randint(0, 120))
        amt = round(random.uniform(200, 5000), 2)
        claim_payments.append((cp_id, c[0], d, amt))
        cp_id += 1

# ============================================================
#  WRITE SQL FILE
# ============================================================
with open("car_insurance_inserts.sql", "w", encoding="utf-8") as f:
    f.write("USE CarInsuranceDB;\n\n")
    for c in customers:
        f.write(f"INSERT INTO Customer VALUES ({c[0]}, '{sql_str(c[1])}', '{sql_str(c[2])}', '{sql_str(c[3])}', '{c[4]}', '{c[5]}');\n")
    for a in agents:
        f.write(f"INSERT INTO Agent VALUES ({a[0]}, '{sql_str(a[1])}', '{a[2]}', '{a[3]}');\n")
    for i, cov in enumerate(COVERAGES, start=1):
        f.write(f"INSERT INTO Coverage VALUES ({i}, '{sql_str(cov[0])}', '{sql_str(cov[1])}');\n")
    for v in vehicles:
        f.write(f"INSERT INTO Vehicle VALUES ({v[0]}, {v[1]}, '{v[2]}', '{v[3]}', {v[4]}, '{v[5]}');\n")
    for p in policies:
        f.write(f"INSERT INTO Policy VALUES ({p[0]}, {p[1]}, {p[2]}, {p[3]}, '{p[4]}', '{p[5]}', '{p[6]}');\n")
    for pc in policy_coverages:
        f.write(f"INSERT INTO PolicyCoverage VALUES ({pc[0]}, {pc[1]});\n")
    for pay in premium_payments:
        f.write(f"INSERT INTO PremiumPayment VALUES ({pay[0]}, {pay[1]}, '{pay[2]}', {pay[3]});\n")
    for cl in claims:
        f.write(f"INSERT INTO Claim VALUES ({cl[0]}, {cl[1]}, '{cl[2]}', '{sql_str(cl[3])}', '{cl[4]}');\n")
    for cp in claim_payments:
        f.write(f"INSERT INTO ClaimPayment VALUES ({cp[0]}, {cp[1]}, '{cp[2]}', {cp[3]});\n")

print("✅ Archivo 'car_insurance_inserts.sql' generado correctamente.")
print(f"Clientes: {len(customers)}, Vehículos: {len(vehicles)}, Pólizas: {len(policies)}, Reclamos: {len(claims)}")
