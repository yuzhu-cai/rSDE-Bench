# VirtualBookPublishing Requirement Document

## 1. Objective
To develop a comprehensive web application named 'VirtualBookPublishing' that allows users to publish virtual books, showcasing their content and author details, with no SQL database requirements, utilizing a local text document for data storage.

## 2. Language
The required development language for this application is Python.

## 3. Page Design

The web application will consist of the following pages:

### Page 1: Login Page
- **Page Title**: Login
- **Page ID**: `loginPage`
  - **Element IDs**:
    - Username Field: `username`
    - Password Field: `password`
    - Login Button: `loginBtn`
    - Registration Link: `registrationLink`
    - About Link: `aboutLink`

*Overview*: This page allows users to log in with their credentials. If they do not have an account, they can navigate to the registration page. They can also navigate to the about page

### Page 2: Registration Page
- **Page Title**: Registration
- **Page ID**: `registrationPage`
  - **Element IDs**:
    - Username Field: `regUsername`
    - Password Field: `regPassword`
    - Submit Button: `regSubmit`
    - Login Link: `loginLink`
  
*Overview*: Users can create a new account by providing a username, password.

### Page 3: Dashboard Page
- **Page Title**: Dashboard
- **Page ID**: `dashboardPage`
  - **Element IDs**:
    - Welcome Message: `welcomeMsg`
    - Create New Book Button: `createBookBtn`: Button to navigate to the Create New Book Page
    - View My Books Button: `viewBooksBtn`: Button to navigate to the View My Books Page
  
*Overview*: Provides an overview for the logged-in user, including options to create a new book or view previously published books.

### Page 4: Create New Book Page
- **Page Title**: Create New Book
- **Page ID**: `createBookPage`
  - **Element IDs**:
    - Title Field: `bookTitle`
    - Author Field: `bookAuthor`
    - Content Area: `bookContent`
    - Submit Button: `submitBook`
    - Cancel Button: `cancelCreate`: Button to cancle book creation and navigate to the Dashboard Page
  
*Overview*: Users can enter the book's title, author, and content, and submit the information to be saved.

### Page 5: View My Books Page
- **Page Title**: My Books
- **Page ID**: `myBooksPage`
  - **Element IDs**:
    - Books List Container: `booksList`
    - View Button (for each book): `viewBook_<index>`(where `<index>` is the number starting from 0)
  
*Overview*: Displays a list of books published by the user, with options to delete or view details for each book.

### Page 6: View Book Details Page
- **Page Title**: Book Details
- **Page ID**: `bookDetailsPage`
  - **Element IDs**:
    - Title Display: `detailTitle`
    - Author Display: `detailAuthor`
    - Content Display: `detailContent`
    - Back Button: `backToMyBooks`
  
*Overview*: Shows the details of a selected book, including title, author, and content, with a return option to the My Books page.

### Page 7: About Page
- **Page Title**: About
- **Page ID**: `aboutPage`
  - **Element IDs**:
    - App Description: `appDescription`
    - Version Info: `versionInfo`
    - Contact Information: `contactInfo`
  
*Overview*: Provides information about the application and ways to contact the support team.

## 4. Data Storage

Data will be stored in the local directory titled `data`, with different types of data organized into separate text files.

### Data Format
- Each file will store information in a structured format, using simple key-value pairs or delimited format (e.g., JSON-style or CSV).

### Example Data Types and Files
1. **User Data** (`data/users.txt`):
   ```
   username1|password1
   username2|password2
   ```
   
2. **Book Data** (`data/books.txt`):
   ```
   bookTitle1|bookAuthor1|bookContent1
   bookTitle2|bookAuthor2|bookContent2
   ```


This structure ensures easy retrieval of user accounts, published books, and session data while maintaining simplicity in local file management.