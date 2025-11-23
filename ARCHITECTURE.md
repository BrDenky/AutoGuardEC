# Estructura Modular de AutoGuardEC

## 📋 Descripción

Este proyecto ha sido refactorizado siguiendo el patrón **Application Factory** de Flask con una arquitectura modular profesional.

## 🏗️ Arquitectura

La aplicación está organizada en los siguientes módulos:

### Configuración
- **`extensions.py`**: Instancias compartidas de SQLAlchemy y Marshmallow
- **`config.py`**: Configuración de la aplicación por entornos

### Modelos (`models/`)
Cada entidad de la base de datos tiene su propio archivo:
- `customer.py` - Clientes
- `vehicle.py` - Vehículos
- `agent.py` - Agentes
- `coverage.py` - Coberturas
- `policy.py` - Pólizas
- `premium_payment.py` - Pagos de primas
- `claim.py` - Reclamos
- `claim_payment.py` - Pagos de reclamos
- `policy_coverage.py` - Relación póliza-cobertura

### Schemas (`schemas/`)
Serialización Marshmallow para cada modelo:
- Un schema por cada modelo
- Manejo de JSON ↔ SQLAlchemy

### Rutas (`routes/`)
Blueprints de Flask organizados por funcionalidad:
- **API Blueprints**: CRUD completo para cada entidad
- **Dashboard Blueprint**: Estadísticas y análisis
- **Frontend Blueprint**: Vistas HTML

## 🚀 Inicio Rápido

### Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env  # Editar según necesidad
```

### Ejecutar la Aplicación

```bash
# Iniciar Docker (base de datos)
docker-compose up -d

# Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📚 API Endpoints

### Clientes
- `GET /api/customers` - Listar clientes (paginado)
- `GET /api/customers/<id>` - Obtener cliente por ID
- `POST /api/customers` - Crear cliente
- `PUT /api/customers/<id>` - Actualizar cliente
- `DELETE /api/customers/<id>` - Eliminar cliente

### Vehículos
- `GET /api/vehicles` - Listar vehículos (paginado)
- `GET /api/vehicles/<id>` - Obtener vehículo por ID
- `POST /api/vehicles` - Crear vehículo
- `PUT /api/vehicles/<id>` - Actualizar vehículo
- `DELETE /api/vehicles/<id>` - Eliminar vehículo

### Pólizas
- `GET /api/policies` - Listar pólizas (paginado)
- `GET /api/policies/<id>` - Obtener póliza por ID
- `POST /api/policies` - Crear póliza
- `PUT /api/policies/<id>` - Actualizar póliza
- `DELETE /api/policies/<id>` - Eliminar póliza

### Agentes
- `GET /api/agents` - Listar agentes (paginado)
- `GET /api/agents/<id>` - Obtener agente por ID
- `POST /api/agents` - Crear agente
- `PUT /api/agents/<id>` - Actualizar agente
- `DELETE /api/agents/<id>` - Eliminar agente

### Coberturas
- `GET /api/coverages` - Listar coberturas (paginado)
- `GET /api/coverages/<id>` - Obtener cobertura por ID
- `PUT /api/coverages/<id>` - Actualizar cobertura
- `DELETE /api/coverages/<id>` - Eliminar cobertura

### Pagos de Primas
- `GET /api/premium_payments` - Listar pagos (paginado)
- `GET /api/premium_payments/<id>` - Obtener pago por ID
- `PUT /api/premium_payments/<id>` - Actualizar pago
- `DELETE /api/premium_payments/<id>` - Eliminar pago

### Reclamos
- `GET /api/claims` - Listar reclamos (paginado)
- `GET /api/claims/<id>` - Obtener reclamo por ID
- `PUT /api/claims/<id>` - Actualizar reclamo
- `DELETE /api/claims/<id>` - Eliminar reclamo

### Pagos de Reclamos
- `GET /api/claim_payments` - Listar pagos de reclamos (paginado)
- `GET /api/claim_payments/<id>` - Obtener pago por ID
- `PUT /api/claim_payments/<id>` - Actualizar pago
- `DELETE /api/claim_payments/<id>` - Eliminar pago

### Dashboard
- `GET /api/dashboard-data` - Obtener estadísticas del sistema

## 🔧 Agregar Nueva Entidad

Para agregar una nueva entidad (ejemplo: `Invoice`):

### 1. Crear el Modelo

```python
# models/invoice.py
from extensions import db

class Invoice(db.Model):
    __tablename__ = 'Invoice'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    
    invoice_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    # ... más campos
```

### 2. Crear el Schema

```python
# schemas/invoice.py
from extensions import ma
from models.invoice import Invoice

class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice
        include_fk = True
        load_instance = True
```

### 3. Crear las Rutas

```python
# routes/invoice.py
from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.invoice import Invoice
from schemas.invoice import InvoiceSchema

invoice_bp = Blueprint('invoices', __name__)

@invoice_bp.route('/api/invoices', methods=['GET'])
def get_invoices():
    # Implementación
    pass
```

### 4. Actualizar `__init__.py`

```python
# models/__init__.py
from models.invoice import Invoice

# schemas/__init__.py
from schemas.invoice import InvoiceSchema

# routes/__init__.py
from routes.invoice import invoice_bp
```

### 5. Registrar Blueprint

```python
# app.py
from routes import invoice_bp
app.register_blueprint(invoice_bp)
```

## 🧪 Testing

```bash
# Verificar importaciones
python -c "from models import Customer; from schemas import CustomerSchema; from routes import customer_bp; print('OK')"

# Ejecutar tests (cuando estén disponibles)
pytest
```

## 📁 Estructura de Archivos

```
AutoGuardEC/
├── app.py                      # Punto de entrada
├── config.py                   # Configuración
├── extensions.py               # Extensiones compartidas
├── models/                     # Modelos SQLAlchemy
│   ├── __init__.py
│   ├── customer.py
│   ├── vehicle.py
│   ├── agent.py
│   ├── coverage.py
│   ├── policy.py
│   ├── premium_payment.py
│   ├── claim.py
│   ├── claim_payment.py
│   └── policy_coverage.py
├── schemas/                    # Schemas Marshmallow
│   ├── __init__.py
│   ├── customer.py
│   ├── vehicle.py
│   ├── agent.py
│   ├── coverage.py
│   ├── policy.py
│   ├── premium_payment.py
│   ├── claim.py
│   ├── claim_payment.py
│   └── policy_coverage.py
├── routes/                     # Blueprints
│   ├── __init__.py
│   ├── customer.py
│   ├── vehicle.py
│   ├── agent.py
│   ├── coverage.py
│   ├── policy.py
│   ├── premium_payment.py
│   ├── claim.py
│   ├── claim_payment.py
│   ├── policy_coverage.py
│   ├── dashboard.py
│   └── frontend.py
├── templates/                  # Templates HTML
├── static/                     # Archivos estáticos
├── Data/                       # Datos
├── .env                        # Variables de entorno
└── requirements.txt            # Dependencias
```

## 🎯 Ventajas de esta Arquitectura

✅ **Mantenibilidad**: Código organizado y fácil de modificar  
✅ **Escalabilidad**: Agregar nuevas funcionalidades es sencillo  
✅ **Testabilidad**: Módulos independientes fáciles de testear  
✅ **Colaboración**: Múltiples desarrolladores sin conflictos  
✅ **Profesionalismo**: Sigue las mejores prácticas de Flask  

## 📝 Notas

- El archivo original `app.py` está respaldado como `app_old_backup.py`
- La funcionalidad de la aplicación no ha cambiado, solo la estructura
- Todos los endpoints mantienen las mismas URLs
- La base de datos requiere Docker corriendo

## 📞 Soporte

Para preguntas o problemas, consulta la documentación de Flask:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Marshmallow Documentation](https://marshmallow.readthedocs.io/)
