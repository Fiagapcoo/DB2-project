# DB2-project

This is a Django-based project for your DB2 practical assignment.

## Getting Started

### Requirements
- Python 3.x
- Django
- PostgreSQL (or SQLite for initial setup)
- psycopg2 (PostgreSQL driver for Python)
- python-decouple (for environment variable management)
- pip (for installing python packages)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Fiagapcoo/DB2-project.git
   cd DB2-project
    ```

2. Create a virtual environment and activate it:

    - On Windows:
    ```bash
    python -m venv venv 
    venv\Scripts\activate
    ```

    - On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables by creating a .env file in the root directory. Here's an example:
    ```
    POSTGRES_DB=your_database_name
    POSTGRES_USER=your_database_user
    POSTGRES_PASSWORD=your_password
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    ```


4. Apply the migrations to set up the database schema:

    ```bash
    python manage.py migrate
    ```

### Running the Project

To run the project, follow the instructions based on your operating system:

#### Windows

1. Run the development server:

    ```bash
    py manage.py runserver
    ```


2. Insert fake data into the database:
    ```bash
    py insertFakeData.py
    ```


#### macOS/Linux


1. Run the development server:

    ```bash
    python3 manage.py runserver
    ```


2. Insert fake data into the database:
    ```bash
    python3 insertFakeData.py
    ```
