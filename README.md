# Embedded Button FSM Simulator

## 📖 Overview

Embedded Button FSM Simulator is a production-style simulation platform designed to emulate real embedded button handling logic using a Finite State Machine (FSM) architecture.

The project reproduces timing-sensitive button interactions commonly implemented in low-level firmware written in C and exposes the behavior through a REST API interface for testing, validation, and automation purposes.

Supported button events:

* Short Click
* Long Click
* Double Click

The platform includes:

* Automated integration testing
* Docker containerization
* CI/CD automation
* Kubernetes deployment support
* Runtime debugging capabilities

---

## 🌐 Live Demo

[https://supreme-fortnight-jj7w7rgrqpqrhp9pw-5000.app.github.dev/ui](https://supreme-fortnight-jj7w7rgrqpqrhp9pw-5000.app.github.dev/ui)

---

## 🏗️ Architecture

```text
app/                    Original embedded C reference logic
simulator/              Python FSM engine + REST API server
tests/                  Automated integration tests (pytest)
k8s/                    Kubernetes deployment manifests
.github/workflows/      GitHub Actions CI/CD pipeline
```

---

## ⚙️ Core Features

* FSM-based embedded button simulation
* Timing-driven event processing
* REST API for hardware event emulation
* Automated integration testing using pytest
* Docker-based containerization
* CI/CD pipeline with GitHub Actions
* Kubernetes deployment support
* Multi-pod runtime visibility and debugging
* Hostname tracing for distributed execution analysis

---

## 🚀 Local Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the simulator

```bash
python simulator/server.py
```

The REST API server will start locally.

---

## 🧪 Automated Testing

Run integration tests:

```bash
pytest tests/
```

Test coverage includes:

* Button press/release sequences
* Short click detection
* Long click timing validation
* Double click recognition
* REST API validation
* FSM transition verification

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

Run the project using Docker Compose:

```bash
docker-compose up --build
```

This will:

* Build the container image
* Launch the simulator service
* Expose the REST API

---

## ☸️ Kubernetes Deployment

Deploy the application:

```bash
kubectl apply -f k8s/
```

Deployment capabilities:

* Deployment and Service configuration
* Multi-replica scaling
* Load balancing across pods
* Runtime pod identification
* Distributed container debugging

---

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline automatically performs:

* Dependency installation
* Automated integration testing
* Container build validation
* CI workflow verification
* Kubernetes manifest validation

Pipeline configuration:

```text
.github/workflows/ci.yml
```

---

## 🧠 DevOps & QA Highlights

* Production-style CI/CD workflow
* Shift-left testing approach
* Automated integration testing
* Containerized infrastructure
* Kubernetes orchestration
* REST-based system validation
* Clear separation between firmware logic and simulation layer
* Debug-oriented runtime observability

---

## 📌 Future Improvements

* Terraform infrastructure provisioning
* Helm chart packaging
* Prometheus and Grafana monitoring
* Load and stress testing
* AWS EKS deployment
* GitOps-based deployment workflow

---

## 👤 Author

**Yura Odegov**

QA Automation Engineer | DevOps-Oriented Engineer
