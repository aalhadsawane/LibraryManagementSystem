# Library Management system with Django
Use Django to execute the following: take in mind that this is strictly only the backend and thus all responses will be REST framework Responses. U can make serializers in a seperate folder as required.

### Models:
Book:
    id (pk)
    Title
    Genre
    Abstract
    Author
    Available (boolean field)

IssueEntry:
    transaction_id (pk)
    book (fk)
    user (fk)
    validator (fk=user [requires role to be staff or admin])
    reissue_count (default=0)
    issue date
    due date
    return date (null=true, default=NULL)
    fine_multiplier
    late_fine
    damage_fine = (0 or 400)
    CONSTANT MAX_REISSUES=2
    CONSTANT DUE_DAYS=14
    constraint: models.UniqueConstraint(
                fields=['book', 'user'],
                condition=models.Q(return_date__isnull=True),
                name='unique_active_entry'
                )

CustomUser:
    id (pk)
    name
    email
    role (choices=["admin", "staff", "member"])


### Logic
Some clarifiction over User roles:

Member has read only permissions.
Staff has read and update permissions (except creating other users).
Admin has read,update and create user permissions.

Thus, any operation which needs updating/creating objects like issuing or returning books can be done with staff and admin only and NOT member.

Reissuing logic:
A reissue allows u to update the due date by 14 days (more specifically the constant due_days).
A reissue can only be done if current date is earlier than the due date.
Only 2 (constant MAX_REISSUES) number of reissues can be done.

### Views:
All views should use appropriate decorators like authentication, permission classes, api_view etc.
All views should be function based views.
U can make new permission classes in a seperate folder if required.

These would be accessible to member:
def login
def get_all_books
def get_available_books
def get_due_books
def get_issue_entries
def get_outstanding_dues
def search_book

These would be accesible to staff:
def login
def get_all_books
def get_available_books
def get_due_books(member_id)
def get_issue_entries(member_id)
def get_outstanding_dues(member_id)
def issue_book
def return_book
def reissue_book
def get_open_issue_entries
def search_book

Some clarification:
- if get_due_books has no member id then it should have the role as member and member_id is just the request.user.id, otherwise if member_id is given the role should be staff or admin.
- issue, return and reissue requires book and member to be passed. the validator is just the request.user

These would be accessible to admin:
def login
def get_all_books
def get_available_books
def get_due_books(member_id)
def get_issue_entries(member_id)
def get_outstanding_dues(member_id)
def issue_book
def return_book
def reissue_book
def create_user
def get_open_issue_entries
def search_book

### Project Directory structure 
django project has the name main
the django app has the name core

### Auth
Use session based auth provided by django.


