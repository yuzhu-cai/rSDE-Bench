# Requirements Document for Digital_Storytelling_Platform

## 1. Objective
Develop a comprehensive web application for a Digital Storytelling Platform that enables users to create, edit, and share their stories without the need for SQL databases.

## 2. Language
The required development language for this task is Python.

## 3. Page Design

### Page 1: Login Page (If the user successfully logs in, redirect them to the Story Creation Page.)
- **Page Title:** User Login
- **Element List:**
  - ID: `username_field`
    - Type: Input
    - Placeholder: "Enter Username"
  - ID: `password_field`
    - Type: Input
    - Placeholder: "Enter Password"
  - ID: `login_button`
    - Type: Button
    - Text: "Login"
  - ID: `register_link`(redirects to the registration page)
    - Type: Link
    - Text: "Create an Account"


## Page 2: Registration Page
- **Page Title:** User Registration
- **Element List:**
  - ID: `reg_username_input`
    - Type: Input
    - Placeholder: "Enter Username"
  - ID: `reg_password_input`
    - Type: Input
    - Placeholder: "Enter Password"
  - ID: `reg_email_input`
    - Type: Input
    - Placeholder: "Enter Email"
  - ID: `register_button`
    - Type: Button
    - Text: "Register"

### Page 3: Story Creation Page
- **Page Title:** Create Your Story
- **Element List:**
  - ID: `story_title_field`
    - Type: Input
    - Placeholder: "Story Title"
  - ID: `story_content_field`
    - Type: Textarea
    - Placeholder: "Write your story here..."
  - ID: `save_story_button`
    - Type: Button
    - Text: "Save Story"





## 4. Data Storage
Data, including user information and stories, will be stored in local text files within a directory named `data`. The data will be managed in the following format:

### Data Format
* User Data: 
  - Format: `username|password` (one user per line)
  - Example:
    ```
    johndoe|password123
    janedoe|securepass456
    ```

* Story Data:
  - Format: `user_id|story_title|story_content` (one story per line, user ID represents the author)
  - Example:
    ```
    johndoe|My First Adventure|Once upon a time in a land far away
    janedoe|The Mysterious Forest|In a dark and enchanted forest
    ```

### File Structure
- Directory: `data/`
  - File 1: `users.txt` (stores user credentials)
  - File 2: `stories.txt` (stores stories created by users)

This structured approach ensures easy access and management of user data and stories without relying on an SQL database.