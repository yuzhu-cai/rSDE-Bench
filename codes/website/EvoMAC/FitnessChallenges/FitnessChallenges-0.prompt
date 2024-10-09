# Requirements Document for 'FitnessChallenges' Web Application

### 1. Objective
The 'FitnessChallenges' web application will provide users with a platform to participate in fitness challenges, track their progress, and share achievements, using a Python-based backend without the need for SQL database storage. Note that the website should start from the login page.

### 2. Language
The development language for the 'FitnessChallenges' web application is Python.

### 3. Page Design

#### Page 1: Login Page
- **Page Title:** User Login
- **Overview:** Allows users to log into their accounts.
- **Elements:**
  - **ID:** `loginForm`  
    **Type:** Form  
  - **ID:** `usernameField`  
    **Type:** Text input (name: username)  
  - **ID:** `passwordField`  
    **Type:** Password input (name: password)  
  - **ID:** `loginButton`  
    **Type:** Button (label: "Login")  

#### Page 2: Dashboard
- **Page Title:** User Dashboard
- **Overview:** Displays user's profile, current challenges, and activity log. 
- **Elements:**
  - **ID:** `userProfile`  
    **Type:** Section  
  - **ID:** `currentChallenges`  
    **Type:** Section: display user's current challenge name
  - **ID:** `activityLog`  
    **Type:** Section: display current user's activity log, donnot display other users'
  - **ID:** `startChallengeButton`  
    **Type:** Button (label: "Start New Challenge") : navigate to Challenges List Page
  - **ID:** `logoutButton`  
    **Type:** Button (label: "Logout")  

#### Page 3: Challenges List
- **Page Title:** Challenges
- **Overview:** Lists available fitness challenges for users to join.
- **Elements:**
  - **ID:** `challengesTable`  
    **Type:** Table  
  - **ID:** `progressButton`  
    **Type:** Button (label: "Progress Tracker"): navigate to Progress Tracker Page

#### Page 4: Progress Tracker
- **Page Title:** Progress Tracker
- **Overview:** Allows users to track their progress and view statistics related to their challenges.
- **Elements:**
  - **ID:** `challengeName`  
    **Type:** Text for displaying user's the names of current challenges 
  - **ID:** `currentProgress`  
    **Type:** Textarea: display user's current progress, it can be clear to update new progress
  - **ID:** `updateProgressButton`  
    **Type:** Button (label: "Update Progress")  
  - **ID:** `Notes`  
    **Type:** Text for displaying user's notes 
  - **ID:** `addNotesField`  
    **Type:** Textarea (name: notes)  

### 4. Data Storage

#### Data Format
All data will be stored in plaintext format in a `.txt` file located in the `data` directory. Each type of data will be segregated into different files for better organization.

#### Example Data Structure
1. **User Login Data (users.txt)**
   - Format: `username:password`
   - Example:
     ```
     johnsmith:password123
     janedoe:supersecurepass
     ```

2. **Challenges Data (challenges.txt)**
   - Format: `challengeName:challengeDescription:challengeDuration`
   - Example:
     ```
     30-Day Yoga Challenge: A month-long yoga journey to improve flexibility and mindfulness: 30 days
     10K Run Challenge: Train to run 10 kilometers in a month: 30 days
     ```

3. **Current Challenges Data (current_challenges.txt)**
   - Format: `username:challengeName`
   - Example:
     ```
     johnsmith:30-Day Yoga Challenge
     ```

4. **User Progress Data (progress.txt)**
   - Format: `username:challengeName:currentProgress:notes`
   - Example:
     ```
     johnsmith:30-Day Yoga Challenge:15 days:Feeling great! Need to improve on morning sessions.
     janedoe:10K Run Challenge:5 days:Completed 2K today. Happy with progress!
     ```

5. **Activity Log (activityLog.txt)**
   - Format: `timestamp:username:activityDescription`
   - Example:
     ```
     2023-10-01 10:00:00:johnsmith:Joined '30-Day Yoga Challenge'
     2023-10-02 11:30:00:janedoe:Updated progress for '10K Run Challenge'
     ```

All files should be created and modified according to the operations performed in the web application, maintaining simplicity and easy readability for user information and activities.