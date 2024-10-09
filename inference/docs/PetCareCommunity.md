# Requirements Document for PetCareCommunity Web Application

## 1. Objective
Develop a web application named 'PetCareCommunity' that serves as a platform for pet owners to connect, share information, and find resources, using Python as the development language to manage data in local text files without the need for SQL. Note that the website should start from the login page.

## 2. Language
The required development language for the PetCareCommunity web application is Python.

## 3. Page Design
This section outlines the elements that should be included on each page, along with their corresponding IDs.
### 3.1 Page 1: Login Page
- **Page Title:** Login
- **IDs and Elements:**
  - `login-page` (div)
  - `username-input` (input[type="text"])
  - `password-input` (input[type="password"])
  - `login-button` (button)

### 3.2 Page 2: Community Feed
- **Page Title:** Community Feed
- **IDs and Elements:**
  - `feed-page` (div)
  - `post-input` (textarea)
  - `post-button` (button)
  - `feed-container` (div)
  - `post-[id]` (dynamic div for each post)
  - `resource-button` (button: navigate to Resources Page)
  - `profile-button` (button: navigate to User Profile Page)

### 3.3 Page 3: Resources
- **Page Title:** Resources
- **IDs and Elements:**
  - `resources-page` (div)
  - `resource-container` (div)
  - `resource-title` (h2) (for each resource)
  - `resource-description` (p) (for each resource)
  - `link` (link) (for external resource links)

### 3.4 Page 4: Profile
- **Page Title:** User Profile
- **IDs and Elements:**
  - `profile-page` (div)
  - `username-display` (h2)
  - `pet-details` (div)
  - `pet-name` (h2) (for current user's pet)
  - `pet-age` (h2) (for current user's pet)
  - `pet-name-input` (input[type="text"])
  - `pet-age-input` (input[type="number"])
  - `save-button` (button)
  - `logout-button` (button: navigate to Login Page)

## 4. Data Storage

### 4.1 Data Format
Data will be stored in text files located in the 'data' directory. Each file will follow a specific format (plain text) and will contain line-separated entries.

#### 4.2 Data Types and Examples
1. **User Data (users.txt):**
   - Format: `username,password`
   - Example:
     ```
     john_doe,password123
     jane_smith,mysecretpassword
     ```

2. **Posts Data (posts.txt):**
   - Format: `post_id,username,timestamp,content`
   - Example:
     ```
     1,john_doe,2023-10-01 12:00:00,I love my golden retriever!
     2,jane_smith,2023-10-02 09:30:00,Just adopted a kitten!
     ```

3. **Resources Data (resources.txt):**
   - Format: `resource_title,resource_description,link`
   - Example:
     ```
     Dog Training Tips,Everything you need to know about training your dog.,http://dogtraining.com
     Pet Nutrition,Learn about the best food for your pets.,http://petnutrition.com
     ```

4. **Profile Data (profiles.txt):**
   - Format: `username,pet_name,pet_age`
   - Example:
     ```
     john_doe,Max,3
     jane_smith,Luna,1
     ```

All data files will be stored in the 'data' directory, ensuring organization and easy access for the application.