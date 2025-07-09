# 📘 Odoo 18 Payment Portal

This repository contains a preconfigured **Odoo 18** instance, including a custom module for managing payments through the web portal. Below you'll find a step-by-step guide to install, configure, and use the project correctly.

---

## 🚀 1. Project Installation

This project uses **Docker** to run the Odoo 18 environment along with its PostgreSQL database.

### 🔧 Prerequisites

Make sure you have the following tools installed on your system:

- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 📥 Clone the repository and run the project with Docker

```bash
git clone https://github.com/LAngel27/payment_portal_odoo.git
cd payment_portal_odoo
docker-compose up --build
```

---

## 🧩 2. Initial Odoo Configuration

Once the containers are running, it's time to access the Odoo interface to perform the initial module setup.

### 🔗 Step 1: Access Odoo from your browser

Open your browser and go to:

👉 [http://localhost:8069/web/database/manager](http://localhost:8069/web/database/manager)

---

### 🛠️ Step 2: Create a new database

On your first visit, you'll see the database creation screen.

Fill out the form with the following fields:

- **Master Password**: Found in the `config/odoo.conf` file under the `admin_passwd` parameter.  
  Example:
  ```ini
  [options]
  admin_passwd = admin
  ```

- **Database Name**: Choose a name for your database. Example: `portal_payment_db`
- **Email**: The superadmin's email. Example: `admin@example.com`
- **Password**: Password for the Odoo admin user.
- **Language**: Select your preferred language.
- **Country**: Select your country.
- (Optional) Check or uncheck **Demo Data** depending on whether you want sample data.

Finally, click the blue **Create database** button to continue.

---

## ⚙️ 3. Module Configuration in the System

Once the database is created and Odoo is running correctly, the next step is to install the custom module in the system.

The module is located at:

```plaintext
extra-addons/payment_portal
```

For a complete guide on how to install, configure, and use this module in Odoo, check the following video:

🎥 **Watch the step-by-step video tutorial for functional module setup**  
👉 [https://video/tutorial](https://app.govideolink.com/blocks/Hb57Msf5WfmpS7dpQcKI/?utm_source=direct&utm_medium=invite_link)

In this video you'll find:

- Activating developer mode  
- Updating the module list  
- Installing the `payment_portal` module  
- Step-by-step configuration of key features for users to access the payment portal
- Accounting features configuration for visualization
---

## 🧑‍💻 Author

Luis Ángel Cartaya Márquez  
📧 luiscartaya27@hotmail.com  
🔗 [GitHub - LAngel27](https://github.com/LAngel27)

---

## 📦 Technologies Used

- Odoo 18
- Docker & Docker Compose
- PostgreSQL 15
- Python 3
- Git
- Odoo Web Library
- AG-Grid (for dynamic data views)
- SASS (as SCSS style preprocessor)

---

## ✅ Supported Use Cases

This project or template allows you to start and maintain module repositories compatible with the following Odoo versions:

- 18.0  

Future versions will be added as they are released, as well as support for previous versions.

---

## 🪪 License

This project is delivered as part of a technical test and is not under a public license.

---
