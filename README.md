# Button Yura – Embedded Button FSM Simulator

##  Overview
This project simulates an embedded button handling system (FSM) using Python.

Originally inspired by real C firmware logic, it reproduces:
- Short Click
- Long Click
- Double Click

The system exposes a REST API for event simulation and includes automated tests.

---

##  Architecture

- app/ – original C logic (reference)
- simulator/ – Python FSM + HTTP server
- tests/ – integration tests using pytest

---

##  API

### POST /event

```json
{
  "button": 1,
  "action": "press"
}