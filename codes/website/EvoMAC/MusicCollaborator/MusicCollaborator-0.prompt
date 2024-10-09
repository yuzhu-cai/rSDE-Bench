# Requirements Document for Music_Collaborator Web Application

## 1. Objective
The objective of the Music_Collaborator web application is to facilitate music collaboration among users by allowing them to create, share, and edit music projects using a user-friendly interface.

## 2. Language
The required development language for the Music_Collaborator web application is Python.

## 3. Page Design
The web application will consist of the following seven pages:

### Page 1: Login Page
**Page Title:** Login  
**Overview:** Users can access their accounts by entering their username and password.  
**Element IDs:**
- `usernameField`: Input field for the username.
- `passwordField`: Input field for the password.
- `loginButton`: Button to submit the login form.
- `registerLink`: Link to redirect to the registration page.
- `aboutLink`: Link to redirect to the About page.
  
### Page 2: Registration Page
**Page Title:** Register  
**Overview:** New users can create an account by filling out a registration form.  
**Element IDs:**
- `regUsernameField`: Input field for the desired username.
- `regPasswordField`: Input field for the desired password.
- `registerButton`: Button to submit the registration form.
- `loginLink`: Link to redirect back to the login page.

### Page 3: Dashboard Page
**Page Title:** Dashboard  
**Overview:** Users can view their projects, create new music projects, and access their profile settings. Each project listed in the `projectList` is clickable, allowing the user to navigate to the corresponding Project Details Page.  
**Element IDs:**
- `projectList`: Display area for the list of user's projects. Each project item is a clickable link that redirects to the respective Project Details Page.
   - `project_<index>`(where `<index>` is the project number starting from 0)
- `createProjectButton`: Button to navigate to the project creation page.
- `profileSettingsLink`: Link to the user profile settings page.

### Page 4: Create Project Page
**Page Title:** Create Project  
**Overview:** Users can create a new music project by entering project details.  
**Element IDs:**
- `projectNameField`: Input field for the project name.
- `projectDescriptionField`: Text area for a project description.
- `collaboratorsField`: Input field for entering collaborator names.
- `createButton`: Button to submit the newly created project.

### Page 5: Project Details Page
**Page Title:** Project Details  
**Overview:** Users can view and edit details of the selected project, including collaborators and project files.  
**Element IDs:**
- `projectDetailView`: Display area for the project overview, including project name and description.
- `collaboratorsList`: Display area for the list of collaborators.
- `musicLinkInputField`: Text Input field for entering the Website Link of the music to be uploaded.
- `uploadFileButton`: Button to upload the selected music file.
- `uploadStatusMessage`: Area to display a message indicating whether the file upload was successful. This message appears only when the upload is successful; no message is shown if the upload fails.


### Page 6: Profile Settings Page
**Page Title:** Profile Settings  
**Overview:** Users can update their account information, such as username and password.  
**Element IDs:**
- `updateUsernameField`: Input field for the updated username.
- `updatePasswordField`: Input field for the updated password.
- `updateButton`: Button to save changes to the profile.

### Page 7: About Page
**Page Title:** About  
**Overview:** Information about the application and its functionalities, along with contact details.  
**Element IDs:**
- `aboutContent`: Display area for the content regarding the application.
- `contactInfo`: Display area for contact details.

## 4. Data Storage
Data will be stored in local text files located in the directory named `data`. Each type of data will be saved in different files for organization purposes. 

### Data Format
- User data will be stored as `users.txt` in the following format:
  ```
  username|password
  ```

- Project data will be stored in `projects.txt` in the following format:
  ```
  project_name|project_description|collaborators
  ```

- Music link data will be stored in `music.txt` in the following format:
  ```
  project_name|music_link
  ```

### Data Examples
**users.txt Example:**
```
john_doe|password123
jane_smith|securepassword
```

**projects.txt Example:**
```
Summer_Song|First collaborative project for summer|john_doe,jane_smith
Winter_Melody|A melody for winter|jane_smith,john_doe
```

**music.txt Example:**
```
Summer_Song|www.example_1.com
Winter_Melody|www.example_2.com
```

This requirements document serves as a comprehensive guide for the implementation of the Music_Collaborator web application to ensure adherence to specifications throughout the development process.