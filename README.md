# spark
“End-to-end creator funnel system for lead capture and automation.”


DAY-1
🚀 Spark Backend System – Architecture & Implementation
This project implements a secure, scalable backend for a Creator Funnel & Client Acquisition platform using modern backend engineering practices.

🧱 Tech Stack
FastAPI – API framework
PostgreSQL – relational database
SQLAlchemy ORM – database modeling & queries
JWT (JSON Web Tokens) – authentication & authorization
Passlib (Argon2) – secure password hashing

🔐 Authentication & Security Layer
Creator Registration
Creators register with name, email, and password
Passwords are never stored directly
Passwords are hashed using Argon2 before saving
Why: prevents credential leaks and meets industry security standards
Creator Login
Email + password validated
Hashed password compared securely
On success, a JWT token is issued
JWT payload contains:
creator ID (sub)
expiration timestamp
Token-Based Authorization
Each protected request requires:
Authorization: Bearer <JWT>

The backend:
Extracts token from request
Verifies signature & expiration
Decodes creator ID
Injects creator into request context
Unauthorized requests automatically return 401.

📦 Database Architecture
All data is relational and integrity enforced using foreign keys.
🧑 Creators Table

Stores:
id (primary key)
name
email (unique)
hashed_password

📋 Leads Table
Linked to creators via:
creator_id → creators.id

Includes:
lead name
email
phone
source

Constraints:
Creator must exist
Duplicate emails per creator prevented

📦 Products Table
Linked to creators:
creator_id → creators.id
Includes:
product name
price
stock

🧾 Orders Table
Linked to products:
product_id → products.id
Includes:
quantity
total amount

⚙️ Core Business Logic
Lead Creation
Validates creator exists
Prevents duplicate leads per creator
Saves lead securely
Order Processing (Atomic)
Validates product exists
Checks available stock
Calculates total = price × quantity
Reduces stock
Commits in single transaction

Prevents:
overselling
inconsistent inventory

🛡 API Protection
All sensitive routes use:
Depends(get_current_user)
Which enforces:
token validation
authentication
access control

No request can modify data without valid JWT.

✅ Data Integrity
Foreign key constraints enforced at database level
Invalid references blocked automatically
Cascading rules understood and managed

🧠 Key Backend Concepts Implemented
Secure password hashing
JWT-based authentication
Middleware-style auth dependencies
Relational schema design
Transaction-safe updates
API validation & error handling
Multi-user system foundation

Production-style security flow
📈 Current System Capabilities
The backend now supports:
✔ Secure creator onboarding
✔ Authenticated login system
✔ Protected APIs
✔ Lead management
✔ Product management
✔ Order processing with stock control
✔ Relational data integrity