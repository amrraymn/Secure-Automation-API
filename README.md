# Secure-Automation-API
A professional Flask-based API designed for small-business automation workflows  
This project streamlines leads management, order tracking, and payments while implementing robust **Security Layers** to protect business data.

## 🛡️ Security Lab Features
I have transformed this automation tool into a **Secure API** by implementing:
* **Token-based Authentication:** Restricts access to authorized users only.
* **Strict Input Validation (Whitelisting):** A robust filtering system that prevents unexpected inputs and malicious attempts (e.g., blocking "HACK" keywords).
* **Security Logging & Monitoring:** Every request (Success/Failure) is logged with IP addresses and Timestamps in `security_logs.txt` for auditing.
* **Defensive Error Handling:** Custom exceptions to prevent information leakage during server errors.

## ✨ Core Business Features
* **Leads Management:** Full CRM for potential customers.
* **Order & Due Tracking:** Real-time tracking of orders and outstanding balances.
* **Automatic Status Updates:** Orders move from `open` to `partial` or `paid` automatically based on payments.
* **SQLite Storage:** Lightweight and reliable database management.
* **JSON Validation:** Powered by Marshmallow for clean data serialization.

## 🛠️ Tech Stack
* **Framework:** Flask
* **ORM:** Flask-SQLAlchemy
* **Validation:** Flask-Marshmallow
* **Database:** SQLite

## 🚀 Quick Start
1. **Install dependencies:**
   ```bash
   python -m pip install -r automation/requirements_automation.txt
Run API:
   python -m automation.app 
Health Check: http://127.0.0.1:8010/health

📂 Project Structure:

-automation/app.py: App factory and secure API routes.

-automation/models.py: Database models and schemas.

-automation_launcher_fixed.py: Desktop/EXE entry point.

-security_logs.txt: Log file for monitoring security events.                         

  my next steps for this API include implementing protections against common attack vectors:

* **DoS/DDoS Mitigation:** Implementing **Rate Limiting** to prevent automated scripts from overwhelming the API with requests.
* **SQL Injection Prevention:** Moving to fully parameterized queries and ORM safety layers to ensure data integrity.
* **Advanced Authentication:** Adding **JWT (JSON Web Tokens)** or **OAuth2** for more robust identity management beyond simple tokens.
* **Brute-Force Protection:** Adding account lockout mechanisms and IP blacklisting for repeated failed attempts.
* **Input Sanitization:** Enhancing validation to prevent **XSS** and other injection attacks through the API parameters
