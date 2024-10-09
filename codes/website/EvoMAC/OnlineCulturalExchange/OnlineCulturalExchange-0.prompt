# Requirements Document for OnlineCulturalExchange

## 1. Objective
The objective of the OnlineCulturalExchange web application is to facilitate cultural exchange among users by providing a user-friendly platform to share and explore global cultures without the need for a SQL database.

## 2. Language
The required development language for this application is Python.

## 3. Page Design

### 3.1. Page Overview
The web application will consist of the following pages:

1. **Login Page**
   - **Page Title**: Login
   - **Element IDs**:
     - `login-form`: Main form container
     - `username`: Username input field
     - `password`: Password input field
     - `login-button`: Submit button
     - `error-message`: Container for error messages
   - **Navigation**:
     - Successful login redirects to the **Home Page**.
     - Unsuccessful login stays on the **Login Page** with an error message.

2. **Home Page**
   - **Page Title**: Home
   - **Element IDs**:
     - `welcome-message`: Welcome message area
     - `culture-list`: List of available cultural exchange topics
       - `culture-item-<index>`(where `<index>` is the number starting from 0): Hyperlink to redirect to specific **Cultural Exchange Pages**
     - `profile-link`: Hyperlink to redirect to the **Profile Page**
     - `contact-link`: Hyperlink to redirect to the **Contact Page**
   - **Navigation**:
     - Users can navigate to the **Profile Page**, or **Contact Page** using the corresponding hyperlinks.
     - Users can navigate to specific **Cultural Exchange Pages** by selecting topics and using the corresponding hyperlinks from the `culture-list`.

3. **Cultural Exchange Page**
   - **Page Title**: Cultural Exchange
   - **Element IDs**:
     - `exchange-form`: Main form for submissions
     - `title`: Title input field for the exchange
     - `description`: Description textarea for details
     - `submit-exchange`: Button to submit the exchange
     - `exchange-list`: List of submitted exchanges
     - `exchange-item`: Individual exchange item display
     - `home-link`: Hyperlink to redirect back to the **Home Page**
   - **Navigation**:
     - Users can return to the **Home Page** using the `home-link`.
  
4. **Profile Page**
   - **Page Title**: Profile
   - **Element IDs**:
     - `profile-header`: Header for user profile
     - `username-display`: Display area for username
     - `logout-button`: Button to log out
     - `home-link`: Hyperlink to redirect back to the **Home Page**
   - **Navigation**:
     - Users can return to the **Home Page** using the `home-link`.
     - Clicking the `logout-button` will redirect the user back to the **Login Page**.

5. **Contact Page**
   - **Page Title**: Contact
   - **Element IDs**:
     - `contact-form`: Main form for contact inquiries
     - `contact-name`: Input field for name
     - `contact-email`: Input field for email address
     - `contact-message`: Textarea for message
     - `send-message-button`: Button to send the message
     - `contact-confirmation`: Area to show submission status
     - `home-link`: Hyperlink to redirect back to the **Home Page**
   - **Navigation**:
     - Users can return to the **Home Page** using the `home-link`.

## 4. Data Storage

### 4.1 Data Format
Data will be stored in local `.txt` files, organized in the `data` directory. The format will be plain text, one entry per line for lists, and comma-separated values for individual records.

### 4.2 Data Examples

- **User Information** (stored in `data/users.txt`):
  ```
  username1,password1
  username2,password2
  ```

- **Cultural Exchange Submissions** (stored in `data/exchanges.txt`):
  ```
  Cultural Title 1,Description of cultural exchange 1
  Cultural Title 2,Description of cultural exchange 2
  ```

- **Contact Messages** (stored in `data/contacts.txt`):
  ```
  Name 1,email1@example.com,Message from user 1
  Name 2,email2@example.com,Message from user 2
  ```

### 4.3 Directory Structure
The application will have the following directory structure for storing data:
```
/OnlineCulturalExchange
  └── data
      ├── users.txt
      ├── exchanges.txt
      └── contacts.txt
```

This structured approach ensures that all user-generated content and interactions are efficiently stored and easily accessible for the application’s operations.