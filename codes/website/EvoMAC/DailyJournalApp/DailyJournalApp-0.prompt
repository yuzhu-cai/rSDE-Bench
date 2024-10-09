# Requirement Document for Daily_Journal_App

## 1. Objective
Develop a web application called "Daily Journal App" that allows users to create, view, and manage journal entries using Python programming language with data stored in local text files.

## 2. Language
The required development language for the Daily Journal App is Python.

## 3. Page Design

### Page 1: Login Page
- **Page Title:** Login
- **Overview:** This page authenticates users. Users must enter their credentials to access their journal entries.If a user does not have an account, they can navigate to the registration page.
  
#### Elements:
- **ID:** `username_input`
  - **Type:** Input Text
  - **Placeholder:** "Enter your Username"
- **ID:** `password_input`
  - **Type:** Input Password
  - **Placeholder:** "Enter your Password"
- **ID:** `register_link`
  - **Type:** Link
  - **Text:** "Don't have an account? Register here"
  - **Destination:** Registration Page
- **ID:** `login_button`
  - **Type:** Button
  - **Text:** "Login"

---

### Page 2: Registration Page
- **Page Title:** Register
- **Overview:** This page allows new users to create an account by registering their credentials.

#### Elements:
- **ID:** `reg_username_input`
  - **Type:** Input Text
  - **Placeholder:** "Choose a Username"
- **ID:** `reg_password_input`
  - **Type:** Input Password
  - **Placeholder:** "Choose a Password"
- **ID:** `register_button`
  - **Type:** Button
  - **Text:** "Register"

---

### Page 3: Dashboard Page
- **Page Title:** Dashboard
- **Overview:** Displays the user's journal entries and provides navigation to create a new entry or log out.
  
#### Elements:
- **ID:** `new_entry_button`
  - **Type:** Button
  - **Text:** "New Entry"
- **ID:** `entry_list`
  - **Type:** Div/List
  - **Description:** Displays a list of journal entries with titles and dates. 
- **ID:** `logout_button`
  - **Type:** Button
  - **Text:** "Logout"

---

### Page 4: New Entry Page
- **Page Title:** New Journal Entry
- **Overview:** Allows users to create a new journal entry and save it to a local text file.

#### Elements:
- **ID:** `entry_title_field`
  - **Type:** Input Text
  - **Placeholder:** "Enter Entry Title"
- **ID:** `entry_content_field`
  - **Type:** Textarea
  - **Placeholder:** "Write your journal entry here..."
- **ID:** `save_entry_button`
  - **Type:** Button
  - **Text:** "Save Entry"

---


## 4. Data Storage

Data for the Daily Journal App will be stored in the local text files located in the directory `data`. Different types of data will be managed using separate text files as follows:

### Data Format
The data will be stored in plain text format, where each journal entry will consist of the title, date, and content structured in the following way:
```
[Entry Title]|[Journal Entry Content]
```

### Data Examples
1. **File:** `data/journal_entries.txt`
```
My First Day|Today was a great day. I started my new job!
Weekend Adventures|Went hiking with friends this weekend. Beautiful weather!
```
2. **File:** `data/user_credentials.txt`
```
user1|password123
user2|mypassword
```
### File Structure
- **Directory:** `data/`
  - **File:** `journal_entries.txt` (for storing all journal entries)
  - **File:** `user_credentials.txt` (optional, for storing user information if needed)

This structure ensures that entries are easily readable and maintainable while allowing the web application to adequately function without the need for a SQL database.