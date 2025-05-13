# OilSpillAI 🛢️🤖

**OilSpillAI** is a cutting-edge web application leveraging machine learning to predict the spread of oil spills in aquatic environments and recommend optimal cleanup strategies. By integrating geospatial analysis, predictive modeling, and interactive visualization, OilSpillAI empowers environmental agencies, cleanup crews, and researchers to make data-driven decisions in emergency response scenarios.

---

## 📋 Table of Contents

1. [🚀 Project Overview](#project-overview)
2. [🔎 Key Features](#key-features)
3. [📐 System Architecture](#system-architecture)
4. [🛠️ Tech Stack](#tech-stack)
5. [💾 Data Requirements](#data-requirements)
6. [⚙️ Installation & Setup](#installation--setup)
7. [🚀 Usage & Examples](#usage--examples)
8. [🧠 Machine Learning Model](#machine-learning-model)
9. [🌐 API Endpoints](#api-endpoints)
10. [🖼️ Visualization Dashboard](#visualization-dashboard)
11. [🤝 Contributing](#contributing)
12. [📄 License](#license)
13. [📞 Contact](#contact)

---

## 🚀 Project Overview

OilSpillAI aims to accelerate environmental response by forecasting oil plume trajectories and identifying high-risk zones. It supports strategic planning for containment and remediation, reducing ecological damage and cleanup costs.

**Objectives:**

* Predict oil spread patterns under varying sea and weather conditions 🌊☀️🌧️
* Provide actionable cleanup recommendations (e.g., booms, skimmers, dispersants) 🧽
* Offer an intuitive dashboard for visualizing predictions and statistics 📊
* Enable secure storage of incident data and imagery 🔒

---

## 🔎 Key Features

* **Predictive Modeling:** Real-time oil spill spread forecasts using trained ML models.
* **Geospatial Analysis:** GIS-based mapping of spill trajectories and impacted zones.
* **Cleanup Advisor:** Data-driven suggestions for optimal remediation techniques.
* **Interactive Dashboard:** Dynamic charts and map overlays for stakeholder insights.
* **Image & Data Storage:** Upload and manage satellite/aerial images via Firebase.
* **User Authentication:** Secure login and role-based access control.

---

## 📐 System Architecture

```plaintext
┌────────────┐     ┌────────────┐     ┌───────────────────┐
│  Frontend  │ ⇄   │   Backend  │ ⇄   │  Machine Learning │
│  (Flask)   │     │  (Flask)   │     │     Engine        │
└────────────┘     └────────────┘     └───────────────────┘
       │                  │                    │
       ▼                  ▼                    ▼
   User UI            REST API            ML Model (TensorFlow)
       │                  │                    │
       ▼                  ▼                    ▼
 GeoJSON & Images   PostgreSQL + PostGIS   Training & Inference
```

---

## 🛠️ Tech Stack

| Layer                | Technology                 |
| -------------------- | -------------------------- |
| **Frontend**         | Flask, Jinja2, HTML5, CSS3 |
| **Backend**          | Python, Flask RESTful API  |
| **Machine Learning** | TensorFlow / scikit-learn  |
| **Database**         | PostgreSQL + PostGIS       |
| **Storage**          | Firebase Storage           |
| **Visualization**    | Leaflet.js, Chart.js       |
| **Containerization** | Docker, docker-compose     |

---

## 💾 Data Requirements

* **Environmental Inputs:**

  * Sea current vectors (u, v) in netCDF or CSV
  * Wind speed & direction data
  * Oil properties (density, viscosity)
* **Geospatial Boundaries:**

  * Coastline shapefiles (GeoJSON)
  * Sensitive ecological zone maps
* **Imagery (optional):**

  * Satellite / drone images in JPG/PNG

> **Note:** Sample datasets are available in `data/samples/` for testing.

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Danchouvzv/OilSpillAI.git
   cd OilSpillAI
   ```

2. **Create Python virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Then edit .env with your settings:
   # FLASK_ENV=development
   # DATABASE_URL=postgresql://user:pass@localhost:5432/oilspill
   # FIREBASE_CREDENTIALS=path/to/firebase.json
   ```

5. **Run database migrations**

   ```bash
   flask db upgrade
   ```

6. **Start the application**

   ```bash
   docker-compose up --build
   # or without Docker:
   flask run --host=0.0.0.0 --port=5000
   ```

Access the dashboard at [http://localhost:5000](http://localhost:5000) 🖥️

---

## 🚀 Usage & Examples

1. **Upload Incident Data** via the web form or API endpoint.
2. **Trigger Prediction**: click “Run Forecast” to compute spill spread.
3. **View Results**: interactive map shows predicted plume for T+1h, T+3h, T+6h.
4. **Download Report**: export CSV or PDF with summary statistics and recommendations.

**API Example:**

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Authorization: Bearer <token>" \
  -F "currents=@data/samples/currents.csv" \
  -F "wind=@data/samples/wind.csv" \
  -F "oil=@data/samples/oil.json"
```

---

## 🧠 Machine Learning Model

* **Model Type:** Convolutional-Recurrent network combining CNN for spatial features and LSTM for temporal dynamics.
* **Training Pipeline:**

  1. Preprocess environmental and geospatial inputs.
  2. Train on historical spill events (2010–2020 data).
  3. Evaluate with RMSE and IoU metrics.
* **Model Files:** Stored in `models/` (e.g., `oil_spill_model.h5`).
* **Retraining:**

  ```bash
  python train.py --config configs/train.yaml
  ```

---

## 🌐 API Endpoints

| Method | Endpoint                 | Description                        |
| ------ | ------------------------ | ---------------------------------- |
| GET    | `/api/status`            | Service health check               |
| POST   | `/api/predict`           | Run spill forecast                 |
| POST   | `/api/upload-image`      | Upload incident imagery to storage |
| GET    | `/api/cleanup-recommend` | Retrieve cleanup strategy advice   |
| POST   | `/api/auth/login`        | Obtain JWT token                   |

---

## 🖼️ Visualization Dashboard

* **Map View:** Leaflet.js–powered map with time-slider for plume animation.
* **Charts:** Chart.js line and bar charts showing spread area vs. time, risk-zone percentages.
* **Reports:** Downloadable PDF summaries via `Download Report` button.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request.

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) and style guidelines.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 📞 Contact

**Danial Omirbek** — *Project Lead*
Email: [talgatovdaniyal@gmail.com](mailto:talgatovdaniyal@gmail.com)
GitHub: [Danchouvzv](https://github.com/Danchouvzv)

Let’s protect our oceans together! 🌊💙
