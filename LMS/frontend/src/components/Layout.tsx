import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';
import {
  BookOpen,
  Home,
  LogOut,
  Users,
  Bell,
  Book,
  Clock,
} from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  // If no user or on login page, just render children
  if (!user || location.pathname === '/login') {
    return <>{children}</>;
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="hidden md:flex md:w-64 md:flex-col">
        <div className="flex flex-col flex-grow pt-5 bg-white overflow-y-auto border-r">
          <div className="flex items-center flex-shrink-0 px-4 mb-5">
            <BookOpen className="h-8 w-8 text-primary mr-2" />
            <span className="text-xl font-bold">LMS</span>
          </div>
          
          <div className="px-4 mb-6">
            <div className="text-sm font-medium text-gray-500">
              Welcome,
            </div>
            <div className="font-medium">
              {user.first_name} {user.last_name}
            </div>
            <div className="text-xs text-muted-foreground mt-1">
              {user.user_type}
            </div>
          </div>
          
          <nav className="flex-1 px-2 pb-4 space-y-1">
            <Link
              to="/dashboard"
              className={`flex items-center px-2 py-2 rounded-md text-sm font-medium ${
                location.pathname === '/dashboard'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <Home className="mr-3 h-5 w-5" />
              Dashboard
            </Link>
            
            <Link
              to="/books"
              className={`flex items-center px-2 py-2 rounded-md text-sm font-medium ${
                location.pathname === '/books'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <Book className="mr-3 h-5 w-5" />
              Books
            </Link>
            
            <Link
              to="/my-issues"
              className={`flex items-center px-2 py-2 rounded-md text-sm font-medium ${
                location.pathname === '/my-issues'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <Clock className="mr-3 h-5 w-5" />
              My Issues
            </Link>
            
            {user.user_type !== 'MEMBER' && (
              <Link
                to="/manage-issues"
                className={`flex items-center px-2 py-2 rounded-md text-sm font-medium ${
                  location.pathname === '/manage-issues'
                    ? 'bg-primary text-primary-foreground'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <BookOpen className="mr-3 h-5 w-5" />
                Manage Issues
              </Link>
            )}

            {user.user_type === 'ADMIN' && (
              <Link
                to="/manage-users"
                className={`flex items-center px-2 py-2 rounded-md text-sm font-medium ${
                  location.pathname === '/manage-users'
                    ? 'bg-primary text-primary-foreground'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <Users className="mr-3 h-5 w-5" />
                Manage Users
              </Link>
            )}
            
            <Link
              to="/notifications"
              className={`flex items-center px-2 py-2 rounded-md text-sm font-medium ${
                location.pathname === '/notifications'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <Bell className="mr-3 h-5 w-5" />
              Notifications
            </Link>
          </nav>
          
          <div className="p-4 mt-auto">
            <Button 
              variant="outline" 
              className="w-full flex items-center justify-center" 
              onClick={handleLogout}
            >
              <LogOut className="mr-2 h-4 w-4" />
              Logout
            </Button>
          </div>
        </div>
      </div>
      
      {/* Main content */}
      <div className="flex flex-col flex-1 overflow-y-auto">
        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
};

export default Layout; 