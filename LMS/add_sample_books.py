import os
import django
import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

from api.models import Book

def add_sample_books():
    # Sample books data
    sample_books = [
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'isbn': '9780743273565',
            'publication_date': datetime.date(1925, 4, 10),
            'genre': 'Fiction',
            'total_copies': 5,
            'available_copies': 5,
            'description': 'A story of wealth, love, and the American Dream in the 1920s.'
        },
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'isbn': '9780061120084',
            'publication_date': datetime.date(1960, 7, 11),
            'genre': 'Fiction',
            'total_copies': 7,
            'available_copies': 7,
            'description': 'A classic of modern American literature about racial inequality in the Deep South.'
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'isbn': '9780451524935',
            'publication_date': datetime.date(1949, 6, 8),
            'genre': 'Dystopian Fiction',
            'total_copies': 4,
            'available_copies': 4,
            'description': 'A dystopian novel about totalitarianism, mass surveillance, and repressive regimentation.'
        },
        {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'isbn': '9780547928227',
            'publication_date': datetime.date(1937, 9, 21),
            'genre': 'Fantasy',
            'total_copies': 6,
            'available_copies': 6,
            'description': 'A fantasy novel about the quest of Bilbo Baggins to win treasure guarded by a dragon.'
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'isbn': '9780141439518',
            'publication_date': datetime.date(1813, 1, 28),
            'genre': 'Romance',
            'total_copies': 3,
            'available_copies': 3,
            'description': 'A romantic novel that follows the character development of Elizabeth Bennet.'
        },
        {
            'title': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'isbn': '9780316769488',
            'publication_date': datetime.date(1951, 7, 16),
            'genre': 'Fiction',
            'total_copies': 4,
            'available_copies': 4,
            'description': 'A story about teenage alienation and loss of innocence.'
        },
        {
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'author': 'J.K. Rowling',
            'isbn': '9780747532743',
            'publication_date': datetime.date(1997, 6, 26),
            'genre': 'Fantasy',
            'total_copies': 8,
            'available_copies': 8,
            'description': 'The first novel in the Harry Potter series about a young wizard.'
        }
    ]

    books_added = 0
    books_skipped = 0

    for book_data in sample_books:
        # Check if book already exists
        if Book.objects.filter(isbn=book_data['isbn']).exists():
            print(f"Book with ISBN {book_data['isbn']} already exists. Skipping.")
            books_skipped += 1
            continue

        # Create the book
        Book.objects.create(**book_data)
        print(f"Added: {book_data['title']} by {book_data['author']}")
        books_added += 1

    print(f"\nSummary: {books_added} books added, {books_skipped} books skipped.")

if __name__ == "__main__":
    print("Adding sample books to the library database...")
    add_sample_books()
    print("Done!") 