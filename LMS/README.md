# Library Management System (LMS)

A comprehensive Library Management System with Django backend, React frontend, and ShadCN UI.

## Features

- Session-based authentication with Django
- Three user types: Member, Staff, and Admin
- Book management (Add, Edit, Remove)
- Book issue and return management
- Notifications system
- Dashboards based on user roles
- RESTful API

## Project Structure

- `api/`: Django REST API backend app
- `frontend/`: React with ShadCN UI frontend

## Setup and Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd LMS
```

2. Activate the virtual environment:
```bash
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Run the development server:
```bash
python manage.py runserver 9000
```

The backend will be available at http://localhost:9000/

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev -- --port 5180
```

The frontend will be available at http://localhost:5180/

## Adding Sample Books

To quickly populate your database with sample books, you can run the provided script:

```bash
python add_sample_books.py
```

This will add 7 classic books to your library system, making it easy to test the application.

## User Types and Permissions

1. **Member**:
   - View and request books
   - View issued and due books
   - Request book reissue (up to 3 times)

2. **Staff**:
   - All Member permissions
   - Approve requests
   - Issue books to members
   - Mark books as returned

3. **Admin**:
   - All Staff permissions
   - Add/edit/delete books
   - Add/remove members and staff

## API Endpoints

- `/api/login/`: Login endpoint
- `/api/logout/`: Logout endpoint
- `/api/users/`: User management
- `/api/books/`: Book management
- `/api/book-issues/`: Book issue management
- `/api/notifications/`: Notifications
- `/api/dashboard-stats/`: Dashboard statistics

## Technologies Used

- **Backend**:
  - Django 5.x
  - Django REST Framework
  - SQLite (can be configured to use PostgreSQL, MySQL, etc.)

- **Frontend**:
  - React 18.x
  - ShadCN UI Components
  - TailwindCSS
  - React Router
  - Axios

## Initial Login

After setting up, you can login with the superuser account that you created during setup:

- Email: [Your Admin Email]
- Password: [Your Admin Password] 