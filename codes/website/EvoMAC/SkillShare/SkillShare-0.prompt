# SkillShare Requirement Document

## 1. Objective
The objective of the SkillShare web application is to allow users to create, share, and manage their skills in a user-friendly environment without utilizing a SQL database, instead relying on local text file storage. Note that the website should start from the login page.

## 2. Language
The required development language for the SkillShare application is Python.

## 3. Page Design

### 1. Login Page
- **Page Title**: Login
- **Overview**: Users can enter their credentials to access their accounts.
- **Elements**:
  - **Username Field**
    - **ID**: `usernameInput`
    - **Type**: text
  - **Password Field**
    - **ID**: `passwordInput`
    - **Type**: password
  - **Login Button**
    - **ID**: `loginButton`
    - **Type**: button
  - **Register Button**
    - **ID**: `registerButton`
    - **Type**: button

### 2. Register Page
- **Page Title**: Register
- **Overview**: Users can enter their credentials to create a new account.
- **Elements**:
  - **Username Field**
    - **ID**: `usernameInput`
    - **Type**: text
  - **Password Field**
    - **ID**: `passwordInput`
    - **Type**: password
  - **Register Button**
    - **ID**: `registerButton`
    - **Type**: button

### 3. Dashboard Page
- **Page Title**: Dashboard
- **Overview**: This is the landing page where users can see featured skills and navigate to other sections.
- **Elements**:
  - **Welcome Message**
    - **ID**: `welcomeMessage`
    - **Type**: paragraph
  - **Featured Skills Section**
    - **ID**: `featuredSkillsSection`
    - **Type**: div: display skills shared by different users.
  - **View All Skills Button**
    - **ID**: `viewAllSkillsButton`
    - **Type**: button
  - **About SkillShare Button**
    - **ID**: `aboutButton`
    - **Type**: button
  - **Profile Link**
    - **ID**: `profileLink`
    - **Type**: link

### 4. Skills Page
- **Page Title**: Skills
- **Overview**: Users can browse, add, or remove skills they are interested in or currently working on.
- **Elements**:
  - **Skills List**
    - **ID**: `skillsList`
    - **Type**: ul: display skills shared by different users.
  - **Add Skill Input**
    - **ID**: `newSkillInput`
    - **Type**: text
  - **Add Skill Button**
    - **ID**: `addSkillButton`
    - **Type**: button
  - **Remove Skill Button**
    - **ID**: `removeSkillButton`
    - **Type**: each skill entry in Skills List has a button.

### 5. Profile Page
- **Page Title**: Profile
- **Overview**: Users can view and edit their profile information and skills.
- **Elements**:
  - **Name Field**
    - **ID**: `usernameInput`
    - **Type**: text: displaying the current user's username, which can be cleared and a new username can be entered
  - **Save Changes Button**
    - **ID**: `saveChangesButton`
    - **Type**: button
  
### 6. About Page
- **Page Title**: About
- **Overview**: Information about SkillShare, its purpose, and how it works.
- **Elements**:
  - **About Section**
    - **ID**: `aboutSection`
    - **Type**: div
  - **Contact Information**
    - **ID**: `contactInfo`
    - **Type**: paragraph

## 4. Data Storage

Data in the SkillShare application is stored in local text files in a directory named `data`. Each type of data is stored in separate files, formatted as plain text lines for easy readability and manipulation.

### Data Files:
1. **User Data**: Stored in `data/users.txt`
   - **Format**: 
     ```
     username,password
     ```
   - **Example**:
     ```
     johnDoe,securePassword123
     ```

2. **Skills Data**: Stored in `data/skills.txt`
   - **Format**: 
     ```
     username:skill1,skill2,skill3
     ```
   - **Example**:
     ```
     johnDoe:Python,JavaScript,HTML
     hhh:abc,edf,mmm
     ```

3. **Profile Data**: Stored in `data/profiles.txt`
   - **Format**: 
     ```
     username
     ```
   - **Example**:
     ```
     johnDoe
     ```

3. **About Data**: Stored in `data/about.txt`
   - **Format**: 
     ```
     information|contact
     ```
   - **Example**:
     ```
     This is a ...|abc@def.com
     ```

### Notes
- Ensure that data is appropriately formatted, and validate user input to prevent errors or corruption of the data files.
- Implement data handling in the Python application to read and write to these text files as needed.
