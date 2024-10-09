# Requirement Document for 'RemoteInternshipMarketplace'

## 1. Objective
Develop a comprehensive web application named 'RemoteInternshipMarketplace' that facilitates the connection between interns and remote internship opportunities while ensuring user information is stored locally in text files. Note that the website should start from the login page.

## 2. Language
The development language required for this project is Python.

## 3. Page Design
This section outlines the elements that should be included on each page, along with their corresponding IDs.

### Page 1: **Login Page**
- **Page Title**: User Login
- **Element IDs**:
  - Input for Username: `input_username`
  - Input for Password: `input_password`
  - Button for Login: `btn_login`
  - Link for Register: `link_register`

### Page 2: **Registration Page**
- **Page Title**: User Registration
- **Element IDs**:
  - Input for Username: `input_username`
  - Input for First Name: `input_first_name`
  - Input for Last Name: `input_last_name`
  - Input for Email: `input_email`
  - Input for Password: `input_password`
  - Input for Confirm Password: `input_confirm_password`
  - Button for Register: `btn_register`

### Page 3: **Dashboard Page**
- **Page Title**: Internships Dashboard
- **Element IDs**:
  - Heading for Welcome Message: `heading_welcome`
  - Button for View Internships: `btn_view_internships` (navigate to Internship Listings Page)
  - Button for Post Internship: `btn_post_internship` (navigate to Post Internship Page)
  - List of Internships: `list_internships` (display all interships' title)
  - Logout Button: `btn_logout`

### Page 4: **Internship Listings Page**
- **Page Title**: Available Internships
- **Element IDs**:
  - Search Input for Internship: `input_search` (input the intership title which you want)
  - Button for Search Intership: `btn_search_intership`
  - List of Search Results: `list_results` (display the searched intership's internship_id, title, description, category, application_deadline)
  - List of Available Internships: `list_available_internships` (display all interships' internship_id and title)
  - Button for View Details (per internship): `btn_view_details_[internship_id]` (navigate to Internship Details Page which display the details information of the selected intership)

### Page 5: **Post Internship Page**
- **Page Title**: Post a New Internship
- **Element IDs**:
  - Input for Internship Title: `input_internship_title`
  - Input for Internship Description: `input_internship_desc`
  - Input for Internship Category: `input_internship_category`
  - Input for Application Deadline: `input_application_deadline`
  - Button for Submit: `btn_submit_internship`

### Page 6: **Internship Details Page**
- **Page Title**: Internship Details
- **Element IDs**:
  - Heading for Internship Title: `heading_internship_title`
  - Paragraph for Internship Description: `para_internship_desc`
  - Paragraph for Internship Category: `para_internship_cate`
  - Paragraph for Internship Deadline: `para_internship_ddl`
  - Button for Apply Now: `btn_apply_now`
  - Button for Back to Listings: `btn_back_to_listings` (navigate to Internship Listings Page)

## 4. Data Storage
Data will be stored Locally in text files within the `data` directory as follows:

- **User Data**: 
  - **File Name**: `users.txt`
  - **Data Format**: `username,password,first_name,last_name,email`
  - **Example Record**: `john_doe,securepassword,John,Doe,john.doe@example.com`

- **Internship Data**: 
  - **File Name**: `internships.txt`
  - **Data Format**: `internship_id,title,description,category,application_deadline`
  - **Example Record**: `1,Software Development Internship,A remote internship in software development,Software,2023-12-31`

- **Internship Applications**:
  - **File Name**: `applications.txt`
  - **Data Format**: `application_id,username,internship_id,application_date`
  - **Example Record**: `1,john_doe,1,2023-10-01`

This structure allows for efficient storage and retrieval of relevant information for the web application's functionalities. Each data type is organized into separate files to maintain clarity and ease of access.