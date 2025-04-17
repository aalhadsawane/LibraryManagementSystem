import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { bookService } from '../services/api';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';

interface Book {
  id: number;
  title: string;
  author: string;
  isbn: string;
  publication_date: string;
  genre: string;
  description: string;
  total_copies: number;
  available_copies: number;
}

const Books: React.FC = () => {
  const { user } = useAuth();
  const [books, setBooks] = useState<Book[]>([]);
  const [filteredBooks, setFilteredBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [requestingBookId, setRequestingBookId] = useState<number | null>(null);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        setIsLoading(true);
        const booksData = await bookService.getAllBooks();
        setBooks(booksData);
        setFilteredBooks(booksData);
      } catch (error) {
        setError('Failed to fetch books. Please try again later.');
        console.error('Error fetching books:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchBooks();
  }, []);

  useEffect(() => {
    if (searchTerm) {
      const filtered = books.filter(
        (book) =>
          book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
          book.author.toLowerCase().includes(searchTerm.toLowerCase()) ||
          book.genre.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredBooks(filtered);
    } else {
      setFilteredBooks(books);
    }
  }, [searchTerm, books]);

  const handleRequestBook = async (bookId: number) => {
    if (!user) return;

    try {
      setRequestingBookId(bookId);
      await bookService.requestBook(bookId);
      
      // Update the book's available copies locally
      setBooks(books.map(book => {
        if (book.id === bookId) {
          return {
            ...book,
            available_copies: book.available_copies - 1
          };
        }
        return book;
      }));
      
      alert('Book requested successfully!');
    } catch (error: any) {
      setError(error.response?.data?.error || 'Failed to request book. Please try again.');
      console.error('Error requesting book:', error);
    } finally {
      setRequestingBookId(null);
    }
  };

  if (isLoading) {
    return <div className="p-8 text-center">Loading books...</div>;
  }

  if (error) {
    return <div className="p-8 text-center text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Books</h1>
        
        {(user?.user_type === 'STAFF' || user?.user_type === 'ADMIN') && (
          <Button>Add New Book</Button>
        )}
      </div>

      <div className="mb-6">
        <Input
          placeholder="Search by title, author, or genre..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="max-w-md"
        />
      </div>

      {filteredBooks.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-lg text-gray-500">No books found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredBooks.map((book) => (
            <Card key={book.id} className="h-full flex flex-col">
              <CardHeader>
                <CardTitle>{book.title}</CardTitle>
                <CardDescription>by {book.author}</CardDescription>
              </CardHeader>
              <CardContent className="flex-grow">
                <div className="space-y-2">
                  <p><span className="font-medium">Genre:</span> {book.genre}</p>
                  <p><span className="font-medium">ISBN:</span> {book.isbn}</p>
                  <p><span className="font-medium">Published:</span> {new Date(book.publication_date).toLocaleDateString()}</p>
                  <p><span className="font-medium">Available:</span> {book.available_copies} of {book.total_copies}</p>
                  {book.description && (
                    <p className="mt-3 text-sm">{book.description}</p>
                  )}
                </div>
              </CardContent>
              <CardFooter>
                {user?.user_type === 'MEMBER' && (
                  <Button
                    disabled={book.available_copies <= 0 || requestingBookId === book.id}
                    onClick={() => handleRequestBook(book.id)}
                    className="w-full"
                  >
                    {requestingBookId === book.id
                      ? 'Requesting...'
                      : book.available_copies <= 0
                      ? 'Not Available'
                      : 'Request Book'}
                  </Button>
                )}
                {(user?.user_type === 'STAFF' || user?.user_type === 'ADMIN') && (
                  <div className="w-full flex gap-2">
                    <Button variant="outline" className="flex-1">Edit</Button>
                    {user?.user_type === 'ADMIN' && (
                      <Button variant="destructive" className="flex-1">Delete</Button>
                    )}
                  </div>
                )}
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Books; 