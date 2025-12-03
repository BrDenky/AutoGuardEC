# 🚗 AutoGuardEC  
**Your peace of mind every mile.**  
_A modern auto insurance management system designed for the Ecuadorian market._

---

## 🧩 Overview
**AutoGuardEC** is a comprehensive **vehicle insurance management platform** that allows users, agents, and administrators to interact with policies, customers, and claims through a centralized dashboard. It was designed to optimize insurance workflows for the **Ecuadorian automotive sector**, combining **data-driven insights**, **secure storage**, and **intuitive interfaces**.

---

## ✨ Key Features
- 🧾 **Policy Management:** Create, update, and track insurance policies.  
- 👥 **Customer Records:** Manage client data with relational database integrity.  
- ⚙️ **Claims Handling:** Log, review, and approve claims efficiently.  
- 📊 **Analytics Dashboard:** Interactive charts and metrics using Flask + Chart.js.  
- 🔐 **Secure Access:** Role-based login for customers, employees, and admins.  
- 🇪🇨 **Localized Design:** Built for Ecuador's auto insurance standards and workflows.

---

## 🏗️ System Architecture
```
Frontend (Bootstrap 5 / HTML / JS)  
        │  
        ▼  
Backend (Flask REST API)  
        │  
        ▼  
Database (MySQL via SQLAlchemy ORM)
```

---

## ⚙️ Tech Stack
| Layer | Technology |
|-------|-------------|
| **Backend** | Python 3.11, Flask, Flask-SQLAlchemy |
| **Database** | MySQL 8 (Dockerized) |
| **Frontend** | HTML5, CSS3, Bootstrap 5, Chart.js |
| **Containerization** | Docker, Docker Compose |
| **Tools** | VS Code, Postman, GitHub |

---

## 🧰 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/brdenky/AutoGuardEC.git
cd AutoGuardEC
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate       # (Linux/Mac)
venv\Scripts\activate          # (Windows)
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run MySQL in Docker
```bash
docker run --name mysqlcontainer10 -e MYSQL_ROOT_PASSWORD=12345 -e MYSQL_DATABASE=autoguardec -p 3306:3306 -d mysql:8.0
```

### 5️⃣ Configure environment variables
Create a `.env` file in the project root:
```env
FLASK_APP=app.py
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:12345@localhost:3306/autoguardec
```

### 6️⃣ Run the app
```bash
flask run
```

---

## 📡 Example API Endpoints
| Method   | Endpoint          | Description                     |
| -------- | ----------------- | ------------------------------- |
| `GET`    | `/policies`       | Retrieve all insurance policies |
| `POST`   | `/customers`      | Add a new customer              |
| `PUT`    | `/claims/<id>`    | Update claim status             |
| `DELETE` | `/employees/<id>` | Remove employee record          |

---

## 📊 Dashboard Preview
### Main View
![alt text](image.png)
### Main Dashboard
![alt text](image-1.png)
### Main Entity Table
![alt text](image-2.png)
### Add Register
![alt text](image-3.png)
### Edit Register
![alt text](image-4.png)
### Delete Register
![alt text](image-5.png)
### PDF report file of customers
![alt text](image-6.png)

FLASK_APP=app.py
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:12345@localhost:3306/autoguardec
```

### 6️⃣ Run the app
```bash
flask run
```

---

## 📡 Example API Endpoints
| Method   | Endpoint          | Description                     |
| -------- | ----------------- | ------------------------------- |
| `GET`    | `/policies`       | Retrieve all insurance policies |
| `POST`   | `/customers`      | Add a new customer              |
| `PUT`    | `/claims/<id>`    | Update claim status             |
| `DELETE` | `/employees/<id>` | Remove employee record          |

---

## 🧪 Testing
Run unit tests with:
```bash
pytest
```
Or API tests with Postman collection (available in `/tests/postman_collection.json`).

---

## 🧑‍💻 Authors

**Mateo Pilaquinga**  
Computer Science Student – Yachay Tech University  
📧 mateo.pilaquinga@yachaytech.edu.ec  
🌐 [LinkedIn](https://linkedin.com/in/pilaquinga-mateo)

**Harolt Farinango**  
Computer Science Student – Yachay Tech University  
📧 harolt.farinango@yachaytech.edu.ec  
🌐 [LinkedIn](https://linkedin.com/in/harolt-farinango)

---

## 🏁 Future Improvements
- Integrate JWT Authentication for role-based access
- Add email notifications for policy renewals
- Implement OCR for automatic claim document scanning
- Deploy to AWS EC2 with Nginx reverse proxy

---

## 📜 License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

  
**Made with ❤️ by the AutoGuardEC Team**

🚗 *Your peace of mind every mile.*
