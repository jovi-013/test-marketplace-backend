# Marketplace API

A RESTful API for a simple e-commerce marketplace application, allowing users to register as buyers or sellers, manage products, and handle orders. This project is to fulfill the requirements of a recruitment process.

**Live API URL:** `https://test-marketplace-backend-production.up.railway.app/`

---

## Tech Stack

* **Language:** Python
* **Framework:** FastAPI
* **Database:** PostgreSQL (hosted on Railway)
* **ORM:** SQLAlchemy (with async support)
* **Data Validation:** Pydantic
* **Authentication:** JWT (JSON Web Tokens) with Passlib for hashing
* **Production Server:** Gunicorn with Uvicorn workers
* **Deployment:** Railway

---

## Features Implemented

-   **User System:** User registration (Buyer, Seller, Admin roles) and login.
-   **Authentication:** Secure JWT-based authentication for protected routes.
-   **Admin Product Management:** Admin-only endpoints for creating master products.
-   **Seller Inventory Management:** Endpoints for sellers to add products from the master list and manage their own price and quantity.
-   **Buyer Product Browse:** Public endpoints to list all products.
-   **Transactional Order System:** Buyers can create orders.
-   **Order History:** Endpoints for viewing order history.

---

## Setup and Local Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jovi-013/test-marketplace-backend/marketplace-backend.git
    cd test-marketplace-backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the environment file:**
    Create a file named `.env` in the root directory and add the these variables below.
    For local development, fill the `DATABASE_URL` like example below.
    
    ```.env
    DATABASE_URL="sqlite+aiosqlite:///./test.db"
    SECRET_KEY="<random_32_byte_hex_string>"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5.  **Run the application:**
    ```bash
    uvicorn marketplace.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

---

## API Endpoints Overview

| Method | Path | Description | Protected |
| :--- | :--- | :--- | :--- |
| `POST` | `/users/` | Create a new user (buyer or seller). | No |
| `POST` | `/users/token` | Log in to get an access token. | No |
| `GET` | `/users/me` | Get details for the current logged-in user. | Yes |
| `GET` | `/products/` | Get a list of all master products. | No |
| `POST`| `/products/` | Create a new master product. | Admin |
| `POST`| `/seller/inventory` | Add a product to a seller's inventory. | Seller |
| `GET` | `/seller/inventory` | Get the current seller's inventory. | Seller |
| `GET` | `/seller/orders` | Get all orders received by the current seller. | Seller |
| `POST`| `/orders/` | Create a new order. | Buyer |
| `GET` | `/orders/my-history` | Get the current buyer's order history. | Buyer |