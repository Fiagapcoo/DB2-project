# DB2-Project: E-commerce Platform

A robust Django-based e-commerce platform developed as a practical assignment for DB2. The project implements a multi-database architecture using PostgreSQL and MongoDB, featuring user authentication, product management, and order processing.

## 🚀 Features

- User authentication and authorization system
- Product catalog with categories and brands
- Shopping cart functionality
- Order management
- Admin dashboard for content management
- Password recovery system
- Email notifications

## 🛠️ Tech Stack

- **Backend Framework:** Django
- **Databases:**
  - PostgreSQL (primary database)
  - MongoDB (complementary storage)
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** Custom authentication system
- **Email Handler:** Custom implementation
- **File Storage:** Cloudinary integration

## 📋 Prerequisites

- Python 3.x
- PostgreSQL
- MongoDB
- pip (Python package manager)

## 🔧 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Fiagapcoo/DB2-project.git
   cd DB2-project
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory like the `.env.example` here is a quick example:
   ```env
   POSTGRES_DB=your_database_name
   POSTGRES_USER=your_database_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

5. **Database Setup**
   ```bash
   # Run the database initialization scripts in order:
   psql -U your_database_user -d your_database_name -f ./database/DDL.sql
   psql -U your_database_user -d your_database_name -f ./database/INSERTS.sql
   
   # Execute all logic objects scripts
   cd database/logic_objects
   for file in */*.sql; do
       psql -U your_database_user -d your_database_name -f "$file"
   done
   ```

6. **Apply Django Migrations**
   ```bash
   python manage.py migrate
   ```

## 🚀 Running the Application

1. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

2. **Access the Application**
   - Open your browser and navigate to `http://localhost:8000`
   - Default admin credentials:
     ```
     Email: joao.silva@email.com
     Password: 123
     ```
   - Default user credentials:
     ```
     Email: maria.oliveira@email.com
     Password: 123
     ```

## 📁 Project Structure

```
.
├── autenticacao/          # Authentication app
├── database/             # Database scripts and schemas
│   ├── DDL.sql
│   ├── INSERTS.sql
│   └── logic_objects/    # Database logic objects
├── email_handler/        # Custom email handling
├── encryption/           # Encryption utilities
├── store/               # Main store application
│   ├── static/          # Static files (CSS, JS, images)
│   └── templates/       # HTML templates
└── project/             # Project configuration
```

## 🔄 Development Workflow

1. **Installing New Dependencies**
   ```bash
   pip install package_name
   pip freeze > requirements.txt
   ```

2. **Database Changes**
   - Add new SQL scripts in the appropriate directory under `database/logic_objects/`
   - Follow the established schema organization (CONTROL, DYNAMIC_CONTENT, etc.)

3. **Running Tests**
   ```bash
   python manage.py test
   ```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is part of an academic assignment. All rights reserved.

## 👥 Authors

- Filipe Correia(@Fiagapcoo)
- James Pereira (@Hazyc)
- Rafael Fernandes (KingOfDeuses)
- João Morgado (@joaomorgado1415)