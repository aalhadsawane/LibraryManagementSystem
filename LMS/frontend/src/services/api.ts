import axios from 'axios';

const API_URL = 'http://localhost:9001/api';

// Create an Axios instance with custom configurations
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // Important for session-based authentication
  headers: {
    'Content-Type': 'application/json',
  },
});

// Authentication Services
export const authService = {
  login: async (email: string, password: string) => {
    const response = await api.post('/login/', { email, password });
    return response.data;
  },
  
  logout: async () => {
    const response = await api.post('/logout/');
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/users/current_user/');
    return response.data;
  },
  
  register: async (userData: any) => {
    const response = await api.post('/users/', userData);
    return response.data;
  },
};

// Book Services
export const bookService = {
  getAllBooks: async () => {
    const response = await api.get('/books/');
    return response.data;
  },
  
  getBook: async (id: number) => {
    const response = await api.get(`/books/${id}/`);
    return response.data;
  },
  
  createBook: async (bookData: any) => {
    const response = await api.post('/books/', bookData);
    return response.data;
  },
  
  updateBook: async (id: number, bookData: any) => {
    const response = await api.put(`/books/${id}/`, bookData);
    return response.data;
  },
  
  deleteBook: async (id: number) => {
    const response = await api.delete(`/books/${id}/`);
    return response.data;
  },
  
  requestBook: async (bookId: number) => {
    const response = await api.post(`/books/${bookId}/request_issue/`);
    return response.data;
  },
};

// Book Issue Services
export const bookIssueService = {
  getMyIssues: async () => {
    const response = await api.get('/book-issues/my_issues/');
    return response.data;
  },
  
  getAllIssues: async () => {
    const response = await api.get('/book-issues/');
    return response.data;
  },
  
  approveIssue: async (issueId: number) => {
    const response = await api.post(`/book-issues/${issueId}/approve/`);
    return response.data;
  },
  
  rejectIssue: async (issueId: number) => {
    const response = await api.post(`/book-issues/${issueId}/reject/`);
    return response.data;
  },
  
  returnBook: async (issueId: number) => {
    const response = await api.post(`/book-issues/${issueId}/return_book/`);
    return response.data;
  },
  
  reissueBook: async (issueId: number) => {
    const response = await api.post(`/book-issues/${issueId}/reissue/`);
    return response.data;
  },
  
  getOverdueBooks: async () => {
    const response = await api.get('/book-issues/overdue/');
    return response.data;
  },
};

// User Management Services
export const userService = {
  getAllUsers: async () => {
    const response = await api.get('/users/');
    return response.data;
  },
  
  getUser: async (id: number) => {
    const response = await api.get(`/users/${id}/`);
    return response.data;
  },
  
  createUser: async (userData: any) => {
    const response = await api.post('/users/', userData);
    return response.data;
  },
  
  updateUser: async (id: number, userData: any) => {
    const response = await api.put(`/users/${id}/`, userData);
    return response.data;
  },
  
  deleteUser: async (id: number) => {
    const response = await api.delete(`/users/${id}/`);
    return response.data;
  },
};

// Dashboard Services
export const dashboardService = {
  getStats: async () => {
    const response = await api.get('/dashboard-stats/');
    return response.data;
  },
};

// Notification Services
export const notificationService = {
  getNotifications: async () => {
    const response = await api.get('/notifications/');
    return response.data;
  },
  
  markAsRead: async (id: number) => {
    const response = await api.post(`/notifications/${id}/mark_as_read/`);
    return response.data;
  },
  
  markAllAsRead: async () => {
    const response = await api.post('/notifications/mark_all_as_read/');
    return response.data;
  },
};

export default api; 