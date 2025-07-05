# 🏏 Smart Self-Training System for Learning Multiple Sports Games

This project is an **AI-powered web application** that helps players improve their techniques in **cricket**, **tennis**, and **badminton**. It uses human pose estimation and machine learning to identify the type of shot from an image and retrieves an instructional video that matches the action.

---

## 🚀 Features

- Upload a photo of a sports shot (e.g., cricket cover drive, badminton smash)
- Detect the shot using **keypoint estimation (Detectron2 + PyTorch)**
- Predict the shot type using a trained ML model
- Fetch and play a matching instructional video stored in MongoDB GridFS
- Separate user roles: **Admin** (uploads videos) and **Player** (uploads images)
- Simple and responsive web interface with FastAPI + Jinja2 templates

---

## 🛠️ Tech Stack

| Category            | Tools / Frameworks                               |
|---------------------|--------------------------------------------------|
| Backend Framework   | FastAPI                                          |
| AI & Vision         | Detectron2, PyTorch                              |
| Database            | MongoDB with GridFS                              |
| Frontend Templating | HTML, CSS, Jinja2                                |
| Storage             | GridFS for large video files                     |
| Tools               | VS Code, Git, GitHub, Jupyter Notebook           |

---

## 📁 Folder Structure

Fastapi_backend/
├── routes/ # API and page routes
├── database/ # MongoDB connection and queries
├── utils/ # Keypoint extraction, model loading
├── static/ # CSS, JS, and static assets
├── templates/ # Jinja2 HTML templates
├── main.py # App entry point
├── .gitignore
├── requirements.txt
└── README.md


---

## ⚙️ How to Run Locally

1. **Clone the repo:**
   ```bash
   git clone https://github.com/IndhumolS/smart_self_training.git
   cd smart_self_training

2. Create a virtual environment and activate it:
     python -m venv venv
     venv\Scripts\activate   # For Windows


3. Install dependencies:
     pip install -r requirements.txt

4. Run the app:
     uvicorn main:app --reload

5. Open your browser and go to:
     http://127.0.0.1:8000

🎓 Academic Context

This project was developed as part of my MCA degree under the theme “Smart Self-Training System for Learning Multiple Sports Games.” It combines machine learning, web development, and real-time video assistance for training in sports.

📜 License
This project is for educational purposes only.

👩‍💻 Author
Indhumol S
📧 indhu2179@gmail.com
🔗 LinkedIn:https://www.linkedin.com/in/indhumol-s-56a9812b8/
🌐 GitHub:https://github.com/IndhumolS

