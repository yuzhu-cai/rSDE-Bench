# Task_Manager Requirements Document

## 1. Objective
Develop a web application called 'Task_Manager' that allows users to create, manage, and track their tasks, using a local text file for data storage.

## 2. Language
The development language required for the Task_Manager web application is **Python**.

## 3. Page Design

### 3.1. Login Page
- **Page Title**: Login
- **Elements**:
  - **Username Input**: 
    - ID: `username_input`
    - Type: Text Field
  - **Password Input**: 
    - ID: `password_input`
    - Type: Password Field
  - **Login Button**: 
    - ID: `login_button`
    - Type: Button
  - **Register Link**:
    - ID: `register_link`
    - Type: Link (redirects to the registration page)

### 3.2. Registration Page
- **Page Title**: User Registration
- **Elements**:
  - **Username Input**:
    - ID: `reg_username_input`
    - Type: Text Field
  - **Password Input**:
    - ID: `reg_password_input`
    - Type: Password Field
  - **Email Input**:
    - ID: `reg_email_input`
    - Type: Text Field
  - **Register Button**:
    - ID: `register_button`
    - Type: Button


### 3.3. Home Page
- **Page Title**: Task Manager Home
- **Elements**:
  - **Task List Display**: 
    - ID: `task_list`
    - Type: List
  - **Add Task Input**: 
    - ID: `add_task_input`
    - Type: Text Field
  - **Due Date Input**: 
    - ID: `due_date_input`
    - Type: Date Field
  - **Add Task Button**: 
    - ID: `add_task_button`
    - Type: Button
  - **Remove Task Button**: 
    - **For each task listed, there will be an associated Remove Button** 
    - ID: `remove_task_button_<task_id>` (each task should have a unique identifier `<task_id>`)
    - Type: Button
  - **Back to Login Button**: 
    - ID: `back_to_login_button`
    - Type: Button
  
## 4. Data Storage

### 4.1. Data Format
Data will be stored in local text files within the directory `data`. The following formats will be used for different types of data:

- **Task Data**: Each task will be stored in a single line format as follows:
  ```
  task_id|task_title|due_date
  ```

- **User Data**: User login credentials may be stored in a separate text file in the format:
  ```
  username|password
  ```

### 4.2. Data Examples
- **Task Data Example**:
  ```
  1|Finish project report|2023-10-31
  2|Grocery shopping|2023-10-15
  ```

- **User Data Example**:
  ```
  johndoe|password123
  janesmith|securepass456
  ```

All data files should be organized in the `data` directory as follows:
```
data/
  tasks.txt      # Contains all task information
  users.txt      # Contains user information
```

This document outlines the essential requirements for the Task_Manager web application, facilitating the development and testing processes.