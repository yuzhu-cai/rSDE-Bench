# Requirements Document for Online Library Management System

## 1. Objective
Develop an Online Library Management System that allows users to manage and access library resources efficiently without utilizing SQL for data storage.

## 2. Language
The required development language for this project is Python.

## 3. Page Design

### 3.1. Page Summary
The application will consist of the following pages:
1. **Login Page**
2. **Registration Page**
3. **Dashboard Page**
4. **Book Management Page**
5. **User Management Page**
6. **Search Page**
7. **Logout Page**

### 3.2. Page Specifications

#### 3.2.1. Login Page
- **Page Title:** Login
- **Element IDs:**
  - Username Field: `login_username`
  - Password Field: `login_password`
  - Login Button: `login_button`
  - Error Message: `login_error`
  - Register Button: `register_button`

#### 3.2.2. Registration Page
- **Page Title:** Register
- **Element IDs:**
  - Username Field: `reg_username_input`
  - Password Field: `reg_password_input`
  - Email Field: `reg_email_input`
  - Register Button: `register_button`

#### 3.2.3. Dashboard Page
- **Page Title:** Dashboard
- **Element IDs:**
  - Welcome Message: `dashboard_welcome`
  - View Books Button: `dashboard_view_books`
  - Manage Users Button: `dashboard_manage_users`
  - Search Books Button: `dashboard_search_books`
  - Logout Button: `dashboard_logout`

#### 3.2.4. Book Management Page
- **Page Title:** Manage Books
- **Element IDs:**
  - Add Book Form: `manage_books_form`
  - Book Title Field: `add_book_title`
  - Author Field: `add_book_author`
  - ISBN Field: `add_book_isbn`
  - Save Book Button: `save_book_button`
  - Delete Book Button: `delete_book_button`
  - Book List Display: `book_list`
  - Book Item ID: `book_item_{id}` (for each book entry)

#### 3.2.5. User Management Page
- **Page Title:** Manage Users
- **Element IDs:**
  - Add User Form: `manage_users_form`
  - Username Field: `add_user_username`
  - Password Field: `add_user_password`
  - Save User Button: `save_user_button`
  - User List Display: `user_list`
  - User Item ID: `user_item_{id}` (for each user entry)

#### 3.2.6. Search Page
- **Page Title:** Search Books
- **Element IDs:**
  - Search Field: `search_field`
  - Search Button: `search_button`
  - Search Results Display: `search_results`
  
#### 3.2.7. Logout Page
- **Page Title:** Logout
- **Element IDs:**
  - Logout Message: `logout_message`
  - Redirect Button: `logout_redirect`

## 4. Data Storage

### 4.1. Data Format
Data will be stored in plain text (*.txt) files with the following formats:
- **Books Data File:** `data/books.txt`
- **Users Data File:** `data/users.txt`

### 4.2. Data Examples

#### 4.2.1. Books Data Format (books.txt)
Each line will contain:
```
Title|Author|ISBN
```
**Example Entries:**
```
The Great Gatsby|F. Scott Fitzgerald|9780743273565
To Kill a Mockingbird|Harper Lee|9780061120084
1984|George Orwell|9780451524935
```

#### 4.2.2. Users Data Format (users.txt)
Each line will contain:
```
Username|Password
```
**Example Entries:**
```
johndoe|password123
janesmith|securepass456
```

### 4.3. Directory Structure
- **Root Directory:**
  - data/
    - books.txt
    - users.txt

This structure will ensure the application can easily access the necessary files for both books and user information while maintaining a clear organization of data.