# VolunteerMatch Requirements Document

## 1. Objective
Develop a web application named 'VolunteerMatch' that connects volunteers with organizations seeking assistance, using Python as the development language, and storing data locally in text files.

## 2. Language
The required development language for the VolunteerMatch web application is Python.

## 3. Page Design
The VolunteerMatch application will consist of the following pages:

### Page 1: Login Page
- **Page Title:** VolunteerMatch - Login
- **ID List:**
    - Login Form: `login-form`
    - Username Field: `username`
    - Password Field: `password`
    - Login Button: `login-button`

**Overview of Content and Functionality:**
- The login page allows users to enter their credentials (username and password).
- The Login button will authenticate users and direct them to the main dashboard if successful.
- An error message will display if the login credentials are incorrect.

### Page 2: Volunteer Dashboard
- **Page Title:** VolunteerMatch - Dashboard
- **ID List:**
    - Header: `dashboard-header`
    - Available Opportunities Section: `available-opportunities`
    - Opportunity Item: `opportunity-{id}` (display the opportunity_title)
    - Apply Button: `apply-button-{id}` (navigate to Opportunity Details Page which contains the details information of the selected opportunity)
    - Logout Button: `logout-button`

**Overview of Content and Functionality:**
- The dashboard displays a list of available volunteer opportunities.
- Each opportunity has an associated Apply button.
- Users can log out via the Logout button.

### Page 3: Opportunity Details Page 
- **Page Title:** VolunteerMatch - Opportunity Details
- **ID List:**
    - Header: `opp-details-header`
    - Description Section: `opp-description`
    - Apply Form: `apply-form`
    - Name Field: `applicant-name`
    - Email Field: `applicant-email`
    - Submit Application Button: `submit-application`

**Overview of Content and Functionality:**
- This page displays detailed information about a selected volunteer opportunity.
- Users can submit their application using the application form provided on this page.
- The application form requires the user’s name and email.

## 4. Data Storage
Data will be stored in plain text format in a directory labeled 'data'. The following files will be created to store different types of data:

### User Credentials
- **File Name:** `data/users.txt`
- **Format:** `username,password`
- **Data Format Example:**
```
username1,password1
username2,password2
```

### Volunteer Opportunities
- **File Name:** `data/opportunities.txt`
- **Format:** `opportunity_id,opportunity_title,opportunity_desc`
- **Data Format Example:**
```
1,Opportunity Title 1,Description of opportunity 1
2,Opportunity Title 2,Description of opportunity 2
```

### Applications
- **File Name:** `data/applications.txt`
- **Format:** `applicant_name,applicant_email,opportunity_id`
- **Data Format Example:**
```
alice,alice@example.com,1
```

**Note:** The application should ensure that data is read from and written to these text files securely and that the format is consistently followed as shown above.