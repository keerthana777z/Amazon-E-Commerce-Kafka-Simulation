Got it, kee 🚀
I’ll craft you a **professional, attractive, and polished README.md** for your repo `Amazon-E-Commerce-Kafka-Simulation`.
It’ll be **eye-catching** with emojis, shields.io badges, clear sections, and a clean developer-focused flow.

Here’s the upgraded version 👇

---

````markdown
# 🛒 Amazon E-Commerce Kafka Simulation  

![React](https://img.shields.io/badge/Frontend-React-blue?style=for-the-badge&logo=react) 
![TailwindCSS](https://img.shields.io/badge/Styling-TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Flask](https://img.shields.io/badge/Backend-Flask-black?style=for-the-badge&logo=flask) 
![Kafka](https://img.shields.io/badge/Event%20Streaming-Kafka-231F20?style=for-the-badge&logo=apache-kafka)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-4EA94B?style=for-the-badge&logo=mongodb) 
![Streamlit](https://img.shields.io/badge/Admin-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Docker](https://img.shields.io/badge/Infra-Docker-2496ED?style=for-the-badge&logo=docker)

---

## 📌 About The Project  

This project is a **real-time, event-driven Amazon-style e-commerce simulation**.  
It demonstrates how **Apache Kafka** can decouple services in a scalable architecture, enabling **instant order placement, tracking, and status updates** — just like modern e-commerce giants.  

👉 Built for **learning, showcasing, and simulating** real-world event-driven e-commerce flows.  

---

## ✨ Features  

### 🛍️ User Portal (React + Tailwind)  
- Interactive **product catalog** with search  
- Bold **Amazon-style price & Add to Cart** button  
- **Cart & Order placement** in real-time  
- **Track order pipeline** (Placed → Shipped → Delivered)  

### ⚡ Backend (Flask + Kafka + MongoDB)  
- Flask API as **entrypoint** for user actions  
- **Apache Kafka** as event broker (decoupled order & status flows)  
- MongoDB for **order persistence**  
- Background Kafka Consumers for **order processing**  

### 🖥️ Admin Dashboard (Streamlit)  
- View all user orders  
- Update status (Placed → Shipped → Delivered)  
- Real-time sync with user portal  

---

## 🏗️ Architecture  

![Architecture Diagram](architecture.png)  
*Note: Add your `architecture.png` file to the repo root for this to display.*  

---

## 🛠️ Tech Stack  

| Layer        | Technology |
|--------------|------------|
| **Frontend** | React, Tailwind CSS |
| **Backend**  | Flask (Python) |
| **Event Bus**| Apache Kafka |
| **Database** | MongoDB |
| **Admin**    | Streamlit |
| **Infra**    | Docker & Docker Compose |

---

## 🚀 Getting Started  

Follow these steps to run the project locally.  

### ✅ Prerequisites  
- Python **3.8+**  
- Node.js & npm  
- Docker & Docker Compose  

### ⚙️ Installation  

1️⃣ Clone the repository  
```bash
git clone https://github.com/keerthana777z/Amazon-E-Commerce-Kafka-Simulation.git
cd Amazon-E-Commerce-Kafka-Simulation
````

2️⃣ Set up backend (Flask)

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3️⃣ Set up frontend (React)

```bash
cd user-portal
npm install
cd ..
```

4️⃣ Run all services

* **Infra (Kafka, Zookeeper, MongoDB)**

```bash
docker-compose up
```

* **Order Consumer**

```bash
python kafka_consumers/order_consumer.py
```

* **Status Consumer**

```bash
python kafka_consumers/status_consumer.py
```

* **Backend API**

```bash
python backend_api/app.py
```

* **User Portal (React)**

```bash
cd user-portal && npm start
```

* **Admin Dashboard**

```bash
streamlit run portals/admin_dashboard.py
```

🖥️ User portal → `http://localhost:3000`
⚙️ Backend API → `http://127.0.0.1:5001`
📊 Admin dashboard → `http://localhost:8501`

---

## 📂 Project Structure

```
├── backend_api/        # Flask API (Kafka Producer)
├── kafka_consumers/    # Consumers for orders & statuses
├── portals/            # Streamlit Admin Dashboard
├── user-portal/        # React Frontend
│   ├── public/
│   └── src/
├── docker-compose.yml  # Kafka, Zookeeper, MongoDB
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .gitignore
```

---



## 📜 License

Distributed under the MIT License. See `LICENSE` for details.

---

