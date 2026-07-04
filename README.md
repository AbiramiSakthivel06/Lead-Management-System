# Lead Management System 🚀

A robust, multi-tenant B2B Lead Management System built using Django and PostgreSQL. This application allows users to track, monitor, and visualize their sales pipeline with strict data isolation.

## 🔗 Live Demo
**[Launch Deployed App](https://lead-management-system-tsl0.onrender.com)**
> ⏳ **Note on Cold Starts:** This application is hosted on a free Render tier. If the app has been idle, the initial page load may take 30–60 seconds while the server spins up.

---

## ✨ Key Features
* **Strict Multi-Tenant Isolation:** Dynamic QuerySet filtering ensures users can only view, create, edit, or delete leads belonging explicitly to their own authenticated accounts.
* **Interactive KPI Dashboard:** High-level metrics tracking total, new, in-progress, and won leads instantly.
* **Data Visualization:** Built-in dynamic Chart.js reporting mapping pipeline distribution by lead status and marketing sources.
* **Advanced Pipeline Filtering:** Real-time text search along with multi-parameter filtering across company metadata, locations, and contacts.
* **Robust Security Design:** Fully protected against CSRF attacks with automated failure routing, secure HTTP headers, and hidden production environment variables.

---

## 🛠️ Tech Stack
* **Backend:** Django (Python)
* **Database:** PostgreSQL (Production)
* **Frontend:** HTML5, Tailwind CSS, JavaScript (Chart.js)
* **Deployment & Hosting:** Render Web Services & Render PostgreSQL
