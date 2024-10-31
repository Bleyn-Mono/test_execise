# Comments App

## Overview

The Comments App is a web application built using Django that allows users to create, view, and manage comments. It features user registration, file uploads, and supports HTML formatting for comments. The application utilizes Bootstrap for responsive design and includes validation for user input.

## Features

- User registration and login
- Comment creation and management
- Nested comments (replies)
- File uploads (images and documents)
- Input validation (email format and comment text)
- Bootstrap styling for a modern UI
- Pagination for comments

## Requirements

- Python 3.x
- Django 5.x
- Other dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository:**

   ```bash
   git clone <https://github.com/Bleyn-Mono/test_execise>
   cd comments-app

2. Create a virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Run migrations:
   ```bash
    pip install -r requirements.txt
   
4. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser

5. Run the development server:
   ```bash
    python manage.py runserver

6. Open the application in your browser:
   Navigate to http://127.0.0.1:8000/comments/.

### Usage
- User Registration: Navigate to the registration page to create a new user account.
- Login: Use your credentials to log in.
- Add Comment: Click on "Add Comment" to submit a new comment.
- File Upload: You can upload images and documents along with your comments.
- Sorting Comments: Use the sorting options to view comments by username, email, or date added.
- Preview Comment: Use the preview feature to see how your comment will look before submitting.

### Contributing
If you want to contribute to the project, feel free to fork the repository and submit a pull request. 
Please ensure to follow the coding standards and include tests for any new features.
