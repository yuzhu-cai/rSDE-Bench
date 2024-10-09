# Requirements Document for RemoteJobBoard

## 1. Objective
Develop a comprehensive web application named 'RemoteJobBoard' that allows users to browse, post, and manage remote job listings. Note that the website should start from the login page.

## 2. Language
The primary development language for this application will be Python.

## 3. Page Design

### Page 1: Login Page
- **Page Title:** Login
- **Overview:** A secure login page for users to authenticate themselves.
- **Elements:**
    - **Username Input (ID: username-input)**: Field for entering the username.
    - **Password Input (ID: password-input)**: Field for entering the password.
    - **Login Button (ID: login-button)**: Submits credentials to log in.
    - **Login Button (ID: register-button)**: Navigate to Register Page.
    - **Error Message Container (ID: error-message)**: Displays error messages if login fails.

### Page 2: Register Page
- **Page Title:** Register
- **Overview:** A secure Register page for users to authenticate themselves.
- **Elements:**
    - **Username Input (ID: username-input)**: Field for entering the username.
    - **Password Input (ID: password-input)**: Field for entering the password.
    - **Login Button (ID: register-button)**: Submits credentials to create a new account.
    - **Error Message Container (ID: error-message)**: Displays error messages if register fails.

### Page 3: Home Page
- **Page Title:** Home
- **Overview:** The initial landing page that welcomes users and offers options to browse job listings or navigate to other sections of the application.
- **Elements:**
    - **Main Content (ID: main-content)**: Displays featured job listings.
    - **Browse Jobs Button (ID: browse-jobs-button)**: Allows users to view all job listings, navigate to Job Listings Page.
    - **Post Job Button (ID: post-job-button)**: Redirects to the job posting page.
    - **Edit Profile Button (ID: edit-profile-button)**: Redirects to the User Profile page.
    - **Login Link (ID: login-link)**: Links to the login page.
  
### Page 4: Job Listings Page
- **Page Title:** Job Listings
- **Overview:** Displays a list of all available remote job postings with options to filter/search.
- **Elements:**
    - **Job List Container (ID: job-list-container)**: Contains individual job postings.
        - Each Job Posting (ID: job-posting-1, job-posting-2, ...): Includes title, company, and summary.
        - **Apply Button for each job posting (ID: apply-button-1, apply-button-2, ...)**: Button to apply for a specific job.
  
### Page 5: Post Job Page
- **Page Title:** Post a Job
- **Overview:** A form for authorized users to post new remote job listings.
- **Elements:**
    - **Job Title Input (ID: job-title-input)**: Field for entering the job title.
    - **Company Name Input (ID: company-name-input)**: Field for entering the company name.
    - **Job Description Textarea (ID: job-description-textarea)**: Area for detailing the job duties.
    - **Submit Button (ID: submit-job-button)**: Button to submit the new job listing.
  
### Page 6: User Profile Page
- **Page Title:** User Profile
- **Overview:** Displays user information and allows for edit functionality.
- **Elements:**
    - **Username Display (ID: username-display)**:  Displaying the current user's username, which can be cleared and a new username can be entered
    - **Email Display (ID: email-display)**:  Displaying the current user's email, which can be cleared and a new email can be entered
    - **Edit Profile Button (ID: edit-profile-button)**: Button to subnmit the revision.
    - **Applied Job List (ID: job-list)**: Display current user's applied jobs.
    - **Logout Button (ID: logout-button)**: Button for users to log out of the application.

## 4. Data Storage

### Overview
Data for the RemoteJobBoard application will be stored in plain text files within the 'data' directory. Each type of data will be stored in a separate file to ensure organization.

### Data Format
- **users.txt**: Contains user information in the following format:
  ```
  username1,password1,email1
  username2,password2,email2
  ```

- **jobs.txt**: Contains job listings in the following format:
  ```
  job_title1,company_name1,job_description1
  job_title2,company_name2,job_description2
  ```

- **applied_jobs.txt**: Contains applied job listings in the following format:
  ```
  username:job_title1,company_name1,job_description1
  username:job_title2,company_name2,job_description2
  ```

### Data Examples
- **users.txt**
  ```
  john_doe,password123,john@example.com
  jane_smith,password456,jane@example.com
  ```

- **jobs.txt**
  ```
  Software Developer,Tech Company,Remote software development position for various projects.
  Project Manager,Business Solutions,Lead and manage teams on remote projects.
  ```

- **applied_jobs.txt**
  ```
  john_doe:Software Developer,Tech Company,Remote software development position for various projects.
  jane_smith:Project Manager,Business Solutions,Lead and manage teams on remote projects.
  ```

### Directory Structure
```
/RemoteJobBoard
    /data
        users.txt
        jobs.txt
        applied_jobs.txt
    app.py
    ...
```

This requirements document provides a clear outline for developing the RemoteJobBoard web application using Python while ensuring proper storage and organizational structure for user and job data.