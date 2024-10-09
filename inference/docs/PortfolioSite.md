# Requirements Document for PortfolioSite

## 1. Objective
Develop a comprehensive web application called 'PortfolioSite' using Python, which consists of at least five pages and stores user information in local text files rather than a SQL database.

## 2. Language
The required development language for 'PortfolioSite' is Python.

## 3. Page Design

### Overview of Pages
The application will consist of the following five pages:

1. **Login Page**
   - **Title:** User Login
   - **Content & Functionality:** Allows users to enter their credentials (username and password) to access the site.
   - **Element IDs:**
     - Input Field for Username: `login_username`
     - Input Field for Password: `login_password`
     - Login Button: `login_button`
     - Error Message Display Area: `login_error_message`
     - Redirect Link to Register: `link_register`

2. **Registration Page**
   - **Title:** User Registration
   - **Content & Functionality:** Facilitates new users in creating an account by filling out a form with their details.
   - **Element IDs:**
     - Input Field for Email: `reg_email`
     - Input Field for Username: `reg_username`
     - Input Field for Password: `reg_password`
     - Register Button: `reg_button`

3. **Portfolio Page**
   - **Title:** User Portfolio
   - **Content & Functionality:** Displays the user's uploaded projects, including links and descriptions.
   - **Element IDs:**
     - Section for Project List: `project_list`
     - Input Field for New Project Link: `new_project_link`
     - Input Field for Project Description: `new_project_description`
     - Add Project Button: `add_project_button`
     - Delete Project Button (for each project): `delete_project_button`
     - Blog Buttion: `blog_button`
     - Contact Buttion: `contact_button`

4. **Blog Page**
   - **Title:** User Blog
   - **Content & Functionality:** Contains a space for users to write and share blog posts.
   - **Element IDs:**
     - Section for Blog Posts: `blog_posts`
     - Input Field for Blog Title: `blog_title`
     - Input Field for Blog Content: `blog_content`
     - Publish Blog Button: `publish_blog_button`
     - Delete Blog Button (for each blog): `delete_blog_button`

5. **Contact Page**
   - **Title:** Contact Information
   - **Content & Functionality:** Provides a contact form for users to send messages.
   - **Element IDs:**
     - Input Field for Name: `contact_name`
     - Input Field for Email: `contact_email`
     - Textarea for Message: `contact_message`
     - Send Message Button: `send_message_button`

## 4. Data Storage

### Data Format
Data will be stored in a structured text format (plain text) within the local directory named 'data'. Each type of data will be stored in a separate text file.

### Data Examples
1. **User Credentials (users.txt)**
   ```
   username1,password1,email1@gmail.com
   username2,password2,email2@gmail.com
   ```

2. **Project Information (projects.txt)**
   ```
   username1,http://example.com/project_link1.com,project_description1
   username1,http://example.com/project_link2.com,project_description2
   ```

3. **Blog Posts (blogs.txt)**
   ```
   username1,blog_title1,blog_content1
   username1,blog_title2,blog_content2
   ```

4. **Contact Messages (contacts.txt)**
   ```
   contact_name1,contact_email1@gmail.com,message_content1
   contact_name2,contact_email2@gmail.com,message_content2
   ```

**Note:** Each line represents an entry with fields separated by commas. Usernames will be used as keys to allow easy retrieval of related projects and blog posts. The structure allows for read/write operations as needed.