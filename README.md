# Library Management System API

A Django REST API for managing a library system with books, users, and issue entries.
To find what urls do what, look into backend/core/urls.py where u will find the functions which are triggered on urls. The functions are defined in backend/core/views.py

Instructions for integrating frontend are at the end of this doc. Instructions for testing with curl are given below, test the curls and add more sample data.

## Setup Instructions

```bash
cd backend
```
### 1. Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## API Testing with cURL

### Important Note About Authentication
Most endpoints require authentication. You must first login to get a session cookie, then use this cookie in subsequent requests.

### Authentication

```bash
# Login (save cookie for subsequent requests)
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}' \
  -c cookies.txt

# Logout
curl -X POST http://localhost:8000/api/logout/ \
  -b cookies.txt
```

### Issue Entries

```bash
# Get all issue entries (Staff/Admin)
curl -X GET http://localhost:8000/api/issues/all/ \
  -b cookies.txt

# Get self user's (ie user which is sending req) issue entries
curl -X GET http://localhost:8000/api/issues/ \
  -b cookies.txt

# Get user's issue entries (Staff/Admin)
curl -X GET http://localhost:8000/api/issues/1/ \
  -b cookies.txt

# Get specific issue entry
curl -X GET http://localhost:8000/api/issues/entry/1/ \
  -b cookies.txt

# Issue book (Staff/Admin) if the model (here IssueEntry) has an fk model(book and user), it should be entered as the pk of that model like bookID and userID are the fk,
curl -X POST http://localhost:8000/api/issue-book/ \
  -H "Content-Type: application/json" \
  -d '{"book":1,"user":2}' \
  -b cookies.txt

# Return book (Staff/Admin)
curl -X POST http://localhost:8000/api/return-book/ \
  -H "Content-Type: application/json" \
  -d '{"book":1,"user":2}' \
  -b cookies.txt

# Reissue book (Staff/Admin)
curl -X POST http://localhost:8000/api/reissue-book/ \
  -H "Content-Type: application/json" \
  -d '{"book":1,"user":2}' \
  -b cookies.txt
```

### Books

```bash
# Get all books
curl -X GET http://localhost:8000/api/books/ \
  -b cookies.txt

# Get single book
curl -X GET http://localhost:8000/api/books/1/ \
  -b cookies.txt

# Get available books
curl -X GET http://localhost:8000/api/books/available/ \
  -b cookies.txt

# Search books
curl -X GET "http://localhost:8000/api/books/search/?q=python" \
  -b cookies.txt
```

### Due Books

```bash
# Get all due books (Staff/Admin)
curl -X GET http://localhost:8000/api/due/all \
  -b cookies.txt

# Get self user's due books
curl -X GET http://localhost:8000/api/due/ \
  -b cookies.txt

# Get given user's due books (Staff/Admin)
curl -X GET http://localhost:8000/api/due/1/ \
  -b cookies.txt
```

### Users (Staff/Admin only)

```bash
# Get all users
curl -X GET http://localhost:8000/api/users/ \
  -b cookies.txt

# Get single user
curl -X GET http://localhost:8000/api/users/1/ \
  -b cookies.txt

# Create user (Admin only)
curl -X POST http://localhost:8000/api/create-user/ \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"userpass123","name":"New User","email":"user@example.com","role":"member"}' \
  -b cookies.txt
```

## Frontend Integration

To connect a frontend application to this API, you need to:

1. Enable CORS for your frontend domain in settings.py (already enabled for development)

2. Include credentials in your fetch requests:

```javascript
// Login
async function login(username, password) {
  const response = await fetch('http://localhost:8000/api/login/', {
    method: 'POST',
    credentials: 'include',  // Important for sending/receiving cookies
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password })
  });
  return await response.json();
}

// Example API call with authentication
async function getBooks() {
  const response = await fetch('http://localhost:8000/api/books/', {
    method: 'GET',
    credentials: 'include',  // Important for sending/receiving cookies
  });
  return await response.json();
}

// Logout
async function logout() {
  const response = await fetch('http://localhost:8000/api/logout/', {
    method: 'POST',
    credentials: 'include',
  });
  return await response.json();
}
```

3. Configure your frontend framework:

```javascript
// For Axios
axios.defaults.withCredentials = true;

// For Angular HttpClient
// In your HTTP requests:
httpClient.get(url, { withCredentials: true });

// For React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      config: {
        credentials: 'include',
      },
    },
  },
});
```

## Role-Based Access

- **Member**: Can view books, search, and view their own issue entries and dues
- **Staff**: Can additionally issue, return, and reissue books, and view all users' data
- **Admin**: Can do everything staff can do, plus create new users

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found

Each error response includes a message explaining what went wrong. 