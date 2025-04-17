# Getting Started with the Library Management System

This guide provides step-by-step instructions to get the Library Management System up and running.

## Prerequisites

Before you begin, make sure you have the following installed:
- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher

## Starting the Backend

1. Navigate to the LMS directory:
```bash
cd LMS
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
# On Windows use: venv\Scripts\activate
```

3. Run the development server:
```bash
python manage.py runserver 9000
```

The server will start at http://localhost:9000/

4. Access the Django admin panel at http://localhost:9000/admin/ using the superuser credentials you created:
   - Email: your-admin-email@example.com
   - Password: your-admin-password

## Starting the Frontend

1. Open a new terminal window

2. Navigate to the frontend directory:
```bash
cd LMS/frontend
```

3. Install dependencies (if you haven't already):
```bash
npm install
```

4. Start the development server:
```bash
npm run dev -- --port 5180
```

The frontend will be accessible at http://localhost:5180/

## Initial Setup

To start using the application, you'll need to create some initial data:

1. Log in to the Django admin panel (http://localhost:9000/admin/)

2. Create user accounts for:
   - Admin users (set user_type to "ADMIN")
   - Staff users (set user_type to "STAFF") 
   - Regular members (set user_type to "MEMBER")

3. Add some books to the library

4. Log in to the frontend application using one of the user accounts you created

## Sample Books

Here are some sample books you can add to get started:

1. **The Great Gatsby**
   - Author: F. Scott Fitzgerald
   - ISBN: 9780743273565
   - Publication Date: 1925-04-10
   - Genre: Fiction
   - Total Copies: 5
   - Description: A story of wealth, love, and the American Dream in the 1920s.

2. **To Kill a Mockingbird**
   - Author: Harper Lee
   - ISBN: 9780061120084
   - Publication Date: 1960-07-11
   - Genre: Fiction
   - Total Copies: 7
   - Description: A classic of modern American literature about racial inequality in the Deep South.

3. **1984**
   - Author: George Orwell
   - ISBN: 9780451524935
   - Publication Date: 1949-06-08
   - Genre: Dystopian Fiction
   - Total Copies: 4
   - Description: A dystopian novel about totalitarianism, mass surveillance, and repressive regimentation.

4. **The Hobbit**
   - Author: J.R.R. Tolkien
   - ISBN: 9780547928227
   - Publication Date: 1937-09-21
   - Genre: Fantasy
   - Total Copies: 6
   - Description: A fantasy novel about the quest of Bilbo Baggins to win treasure guarded by a dragon.

5. **Pride and Prejudice**
   - Author: Jane Austen
   - ISBN: 9780141439518
   - Publication Date: 1813-01-28
   - Genre: Romance
   - Total Copies: 3
   - Description: A romantic novel that follows the character development of Elizabeth Bennet.

## User Types and Capabilities

1. **Member**:
   - Browse books
   - Request books
   - View issued books
   - Request reissues (up to 3 times)
   - View notifications

2. **Staff**:
   - All Member capabilities
   - Process book requests (approve/reject)
   - Issue books to members
   - Mark books as returned
   - View overdue books

3. **Admin**:
   - All Staff capabilities
   - Add/edit/delete books
   - Manage user accounts
   - Access to system statistics

## API Documentation

The backend provides a RESTful API with the following endpoints:

- `/api/login/`: Login endpoint
- `/api/logout/`: Logout endpoint
- `/api/users/`: User management
- `/api/books/`: Book management
- `/api/book-issues/`: Book issue management
- `/api/notifications/`: Notifications
- `/api/dashboard-stats/`: Dashboard statistics

## Troubleshooting

1. **CORS Issues**: If you encounter CORS errors, make sure the backend server is running and that the frontend is making requests to the correct URL (http://localhost:9000/api/).

2. **Authentication Problems**: Ensure the credentials you're using are correct and that the user account is active.

3. **Database Issues**: If you need to reset the database, run:
   ```bash
   python manage.py flush
   ```
   Then create a new superuser with:
   ```bash
   python manage.py createsuperuser
   ```

4. **Missing Dependencies**: If you encounter missing dependency errors, run:
   ```bash
   pip install -r requirements.txt
   ```
   For frontend:
   ```bash
   npm install
   ``` 