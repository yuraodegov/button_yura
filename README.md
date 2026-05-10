# Embedded Button FSM Simulator

## 📖 Overview

Production-style simulation platform for embedded button handling logic based on a Finite State Machine (FSM) architecture.

Originally inspired by real embedded firmware behavior written in C, this project reproduces timing-based button interactions and exposes them through a REST API interface.

Supported events:

* Short Click
* Long Click
* Double Click

The project includes automated integration testing, containerized deployment, and CI/CD automation.

---

## 🌐 Live Demo

[http://ec2-13-60-47-3.eu-north-1.compute.amazonaws.com:5000/ui](https://ominous-system-69575vpv4j7j24q9q-5000.app.github.dev/ui)

---

## 🏗️ Project Architecture

```text
app/                    Original C reference logic
simulator/              Python FSM engine + REST API server
tests/                  Automated integration tests (pytest)
k8s/                    Kubernetes manifests
.github/workflows/      GitHub Actions CI pipeline
```

---

## ⚙️ Core Features

* FSM-based embedded button simulation
* REST API for hardware-event emulation
* Timing-based event processing
* Automated integration testing with pytest
* Docker containerization
* CI/CD pipeline using GitHub Actions
* Kubernetes deployment support
* Multi-pod runtime debugging and hostname tracing

---

## 🚀 Run Locally

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start simulator

```bash
python simulator/server.py
```

Server will start locally and expose the REST API.

---

## 🧪 Automated Testing

Run integration tests:

```bash
pytest tests/
```

Test coverage includes:

* Button press/release flows
* Short click detection
* Long click timing validation
* Double click recognition
* API-level verification

---

## 🌐 REST API

### POST /event

Simulate button interaction:

```json
{
  "button": 1,
  "action": "press"
}
```

### Example Response

```json
{
  "button": 1,
  "event": "SHORT_CLICK",
  "duration": 0.12
}
```

---

## 🐳 Docker Deployment

Run using Docker Compose:

```bash
docker-compose up --build
```

This will:

* Build the container image
* Launch the simulator service
* Expose the REST API

---

## ☸️ Kubernetes Deployment

Example deployment:

```bash
kubectl apply -f k8s/
```

Features:

* Deployment + Service configuration
* Multi-replica scaling
* Load balancing across pods
* Runtime pod identification

---

## 🔄 CI/CD Pipeline

GitHub Actions pipeline automatically performs:

* Dependency installation
* Automated testing
* Container build validation
* CI workflow verification

Pipeline configuration:

```text
.github/workflows/ci.yml
```

---

## 🧠 DevOps Highlights

* Production-like CI/CD workflow
* Automated integration testing
* Containerized infrastructure
* Kubernetes orchestration
* REST-based system validation
* Separation between firmware logic and simulation layer
* Debug-oriented runtime visibility

---

## 📌 Future Improvements

* Terraform infrastructure provisioning
* Helm charts
* Prometheus + Grafana monitoring
* Load and stress testing
* AWS EKS deployment

---

## 👤 Author

Yura Odegov

QA Automation Engineer | DevOps-oriented Engineer
