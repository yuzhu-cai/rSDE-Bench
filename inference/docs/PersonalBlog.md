# Requirement Document for 'Personal_Blog' Web Application

## 1. Objective
The objective of the 'Personal_Blog' web application is to provide users with a simple platform to create, manage, and share their personal blog entries without relying on a database; all data will be stored locally in text files.

## 2. Language
The required development language for this application is **Python**.

## 3. Page Design

### 3.1. Login Page
- **Page Title:** User Login
- **ID List:**
  - **Username Input:** `username_input`
  - **Password Input:** `password_input`
  - **Login Button:** `login_button`
  - **Message Display:** `login_message`
  - **Register Link:** `register_link`
- **Overview:** This page allows users to enter their credentials to access the blog. Upon successful login, users will be redirected to the main blog page. If unsuccessful, an error message will be displayed.

### 3.2. Registration Page
- **Page Title:** User Registration
- **ID List:**
  - **Username Input:** `reg_username_input`
  - **Password Input:** `reg_password_input`
  - **Email Input:** `reg_email_input`
  - **Register Button:** `register_button`
  - **Message Display:** `register_message`
- **Overview:** This page allows users to register their accounts to access the blog. Upon successful register, users will be redirected to the main blog page. If unsuccessful, an error message will be displayed.

### 3.3. Main Blog Page
- **Page Title:** My Personal Blog
- **ID List:**
  - **Blog Title Display:** `blog_title`
  - **New Post Button:** `new_post_button`
  - **View Post Button:** `view_post_button`
  - **Post List Display:** `post_list`
  - **Logout Button:** `logout_button`
  - **Message Display:** `blog_message`
- **Overview:** This page displays the list of blog posts. Users can create a new post or view existing ones. There's an option to logout from the application.

### 3.4. New Post Page
- **Page Title:** Create New Post
- **ID List:**
  - **Post Title Input:** `post_title_input`
  - **Post Content Area:** `post_content_area`
  - **Submit Post Button:** `submit_post_button`
  - **Message Display:** `post_message`
- **Overview:** This page allows users to create a new blog post by providing a title and content. After submitting, the new post will be saved and the user will be redirected back to the main blog page.

### 3.5. View Post Page
- **Page Title:** View Blog Post
- **ID List:**
  - **Post Title Display:** `view_post_title`
  - **Post Content Display:** `view_post_content`
  - **Edit Post Button:** `edit_post_button`
  - **Delete Post Button:** `delete_post_button`
  - **Back to Blog Button:** `back_to_blog_button`
- **Overview:** This page displays the full content of a selected blog post with options to edit or delete the post. Users can navigate back to the main blog page from here.

### 3.6. Edit Post Page
- **Page Title:** Edit Blog Post
- **ID List:**
  - **Post Title Input:** `post_title_input`
  - **Post Content Input:** `post_content_input`
  - **Submit Post Button:** `submit_post_button`
  - **Back to Blog Button:** `back_to_blog_button`
- **Overview:** This page displaysrhe tile and the full content of a selected blog post in two fields. Users can edit the post in the fields and submit their revision and navigate back to the main blog page from here.

## 4. Data Storage

The application will store data in local text files located in the directory **'data'**. The different types of data will be organized into separate files as follows:

### 4.1. User Data
- **File Name:** `users.txt`
- **Data Format:** `username,password`
- **Data Example:**
  ```
  john_doe,password123
  jane_smith,securepass
  ```

### 4.2. Blog Posts
- **File Name:** `posts.txt`
- **Data Format:** `post_title|post_content`
- **Data Example:**
  ```
  My First Blog Post|This is the content of my very first blog post.
  Exploring Python|Python is an amazing programming language that is versatile and easy to learn.
  ```

### 4.3. Log Files
- **File Name:** `logs.txt`
- **Data Format:** `timestamp|event`
- **Data Example:**
  ```
  2023-10-01 10:00:00|User john_doe logged in.
  2023-10-01 10:05:00|User john_doe created a new post titled 'My First Blog Post'.
  ```

This structured data storage will facilitate easy data retrieval and management through simple file manipulations in Python, ensuring the application remains light and efficient without the need for a SQL database.