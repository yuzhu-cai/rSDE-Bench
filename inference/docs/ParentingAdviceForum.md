# Requirements Document for ParentingAdviceForum

## 1. Objective
The ParentingAdviceForum is a web application designed to provide a platform for parents to share, seek, and offer advice on various parenting topics. Note that the website should start from the login page.

## 2. Language
The required development language for the ParentingAdviceForum is Python.

## 3. Page Design
This section outlines the elements that should be included on each page, along with their corresponding IDs. The web application will consist of the following seven pages:

### 1. Login Page
- **Page Title**: Login
- **Elements**:
  - **Username Input Field**: 
    - ID: `username-input`
  - **Password Input Field**: 
    - ID: `password-input`
  - **Login Button**: 
    - ID: `login-button`
  - **Register Button**: 
    - ID: `register-button`
  

### 2. Register Page
- **Page Title**: Register
- **Elements**:
  - **Username Input Field**: 
    - ID: `username-input`
  - **Password Input Field**: 
    - ID: `password-input`
  - **Register Button**: 
    - ID: `register-button`

### 3. Home Page
- **Page Title**: Home
- **Elements**:
  - **Welcome Message**: 
    - ID: `welcome-message`
  - **Navigation Links**:
    - **Forum Link**: 
      - ID: `forum-link` (navigate to Forum Page)
    - **Post Advice Link**: 
      - ID: `post-advice-link` (navigate to Post Advice Page)
    - **My Account Link**: 
      - ID: `my-account-link` (navigate to My Account Page)
    - **Contact Us Link**: 
      - ID: `contact-us-link` (navigate to Contact Us Page)
  - **Recent Posts Section**: 
    - ID: `recent-posts` (display posts' tiltes and contents)

### 4. Forum Page
- **Page Title**: Forum
- **Elements**:
  - **Discussion Threads List**: 
    - ID: `thread-list` (dispaly thread_id, thread_title, thread_content, and username)
  - **Create view Thread Button**: 
    - ID: `view-thread-button` 
  - **Thread Title Input Field**: 
    - ID: `thread-title-input` (navigate to View Thread Page, and each thread has suach a button)
  - **Thread Content Input Area**: 
    - ID: `thread-content-area`
  - **Submit Button**: 
    - ID: `submit-thread-button`
  
### 5. View Thread Page
- **Page Title**: View Thread
- **Elements**:
  - **Thread Title Display**: 
    - ID: `view-thread-title`
  - **Thread Content Display**: 
    - ID: `view-thread-content`
  - **Comments Section**: 
    - ID: `comments-section`
  - **Comment Input Area**: 
    - ID: `comment-input-area`
  - **Submit Comment Button**: 
    - ID: `submit-comment-button`

### 6. Post Advice Page
- **Page Title**: Post Advice
- **Elements**:
  - **Advice Title Input Field**: 
    - ID: `advice-title-input`
  - **Advice Content Input Area**: 
    - ID: `advice-content-area`
  - **Submit Advice Button**: 
    - ID: `submit-advice-button`

### 7. My Account Page
- **Page Title**: My Account
- **Elements**:
  - **User Information Display**: 
    - ID: `user-info-display` (textarea displays username, which can be clear to input a new name)
  - **Edit Profile Button**: 
    - ID: `update-profile-button`
  - **Delete Account Button**: 
    - ID: `delete-account-button`

### 8. Contact Us Page
- **Page Title**: Contact Us
- **Elements**:
  - **Name Input Field**: 
    - ID: `contact-name-input`
  - **Email Input Field**: 
    - ID: `contact-email-input`
  - **Message Input Area**: 
    - ID: `contact-message-area`
  - **Send Message Button**: 
    - ID: `send-message-button`
  - **Confirmation Message Display**: 
    - ID: `confirmation-message`

## 4. Data Storage
Data in the ParentingAdviceForum will be stored in local text files located in the directory `data`. Each type of data will be appropriately categorized into different files.

### Data Formats and Example Data
1. **Users** (stored in `data/users.txt`):
   - **Format**: `username,password`
   - **Example Data**:
     ```
     john_doe,password123
     jane_smith,securepass456
     ```

2. **Threads** (stored in `data/threads.txt`):
   - **Format**: `thread_id,thread_title,thread_content,username`
   - **Example Data**:
     ```
     1,Best Baby Names,Looking for unique baby name ideas!,john_doe
     2,Potty Training Tips,Any tips for a smooth potty training?,jane_smith
     ```

3. **Comments** (stored in `data/comments.txt`):
   - **Format**: `comment_id,thread_id,comment_content,username`
   - **Example Data**:
     ```
     1,1,How about the name "Sophie"?,jane_smith
     2,2,Start with a schedule!,john_doe
     ```

4. **Advice Posts** (stored in `data/advice_posts.txt`):
   - **Format**: `advice_id,advice_title,advice_content,username`
   - **Example Data**:
     ```
     1,Dealing with Sleep Issues,Establish a bedtime routine.,john_doe
     2,Healthy Eating Habits,Introduce vegetables early!,jane_smith
     ```

5. **Contact imformations** (stored in `data/contact.txt`):
   - **Format**: `contact_id,contact_name,contact_email,contact_messgae,username`
   - **Example Data**:
     ```
     1,editor,jd@example.com,this is a test,john_doe
     2,editor,jd@example.com,this is a test too,jane_smith
     ```

All data will be appended to the respective text files when new records are created, ensuring that previously stored information remains intact.