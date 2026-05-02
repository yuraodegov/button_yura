# Button Yura – Embedded Button FSM Simulator

## 📖 Overview

This project simulates an embedded button handling system (Finite State Machine) using Python.

Originally inspired by real C firmware logic, it reproduces:

* Short Click
* Long Click
* Double Click

The system exposes a REST API for event simulation and includes automated integration tests.

---

## 🏗️ Architecture

* `app/` – original C logic (reference implementation)
* `simulator/` – Python FSM + HTTP server
* `tests/` – integration tests using pytest
* `.github/workflows/` – CI/CD pipeline

---

## 🚀 How to Run

### Run locally

```bash
pip install -r requirements.txt
python simulator/server.py
```

Server will start and listen for incoming HTTP requests.

---

### Run tests

```bash
pytest tests/
```

---

## 🌐 API

### POST /event

Send button action:

```json
{
  "button": 1,
  "action": "press"
}
```

### Example response

```json
{
  "button": 1,
  "event": "SHORT_CLICK",
  "duration": 0.12
}
```

---

## 🐳 Docker

Run the project using Docker Compose:

```bash
docker-compose up --build
```

This will:

* build the container
* start the simulator service
* allow API interaction

---

## ⚙️ CI/CD

This project uses GitHub Actions pipeline:

Pipeline steps:

* Install dependencies
* Run automated tests (pytest)
* Validate system behavior

CI configuration:

```
.github/workflows/ci.yml
```

---

## 🧪 Testing

* Framework: `pytest`
* Type: integration testing
* Covers:

  * button press/release flows
  * timing-based events (short/long/double click)
  * API-level validation

---

## 🧠 DevOps Highlights

* Automated testing with pytest
* CI pipeline with GitHub Actions
* Containerized environment (Docker)
* Clear separation between firmware logic and simulation layer
* REST-based interaction for system testing

---

## 📌 Future Improvements

* Kubernetes deployment (k8s manifests)
* Infrastructure as Code (Terraform)
* Monitoring (Prometheus + Grafana)
* Load testing

---

## 👤 Author

Yura Odegov
QA Engineer / DevOps-oriented Engineer
