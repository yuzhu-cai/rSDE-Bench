# Requirement Document for Movie Recommendation System

## 1. Objective
To develop a web application that recommends movies to users based on their preferences, utilizing Python for development and local text file storage for data management.

## 2. Language
The required development language for the Movie Recommendation System is Python.

## 3. Page Design

### a. Login Page
- **Page Title:** User Login
- **Elements:**
  - **Login Form**
    - **ID:** `loginForm`
    - **Username Field**
      - **ID:** `usernameField`
    - **Password Field**
      - **ID:** `passwordField`
    - **Login Button**
      - **ID:** `loginButton`
    - **Error Message Display**
      - **ID:** `errorMessage`
    - **Link to Registration page**
      - **ID:** `registerLink`

### b. Registration Page
- **Page Title:** User Register
- **Elements:**
  - **Register Form**
    - **ID:** `registerForm`
    - **Username Field**
      - **ID:** `usernameField`
    - **Password Field**
      - **ID:** `passwordField`
    - **Register Button**
      - **ID:** `registerButton`
    - **Error Message Display**
      - **ID:** `errorMessage`

### c. Home Page
- **Page Title:** Movie Recommendations
- **Elements:**
  - **Welcome Message**
    - **ID:** `welcomeMessage`
  - **Search Button**
    - **ID:** `searchButton`
  - **My Favorites Button** (navigate to Favorites Page)
    - **ID:** `favoriteButton`
  - **Recommendations List**
    - **ID:** `recommendationsList`
  - **View Details Button** (for each movie in the recommendations)
    - **ID:** `viewDetailsButton_[movieID]` (where `[movieID]` is the unique identifier for each movie)

### d. Search Page
- **Page Title:** Search Movies
- **Elements:**
  - **Search Field**
    - **ID:** `searchField`
  - **Search Button**
    - **ID:** `searchButton`
  - **Search Results Display**
    - **ID:** `searchResult`
 
### e. Movie Details Page
- **Page Title:** Movie Details
- **Elements:**
  - **Movie Title**
    - **ID:** `movieTitle`
  - **Movie Description**
    - **ID:** `movieDescription`
  - **Rating Display**
    - **ID:** `movieRating`
  - **Add to Favorites Button**
    - **ID:** `addToFavoritesButton`
  - **Back to Home Button**
    - **ID:** `backToHomeButton`

### f. Favorites Page
- **Page Title:** Favorite Movies
- **Elements:**
  - **Favorites List**
    - **ID:** `favoritesList`
  - **View Details Button** (for each favorite movie)
    - **ID:** `favoriteViewDetailsButton_[movieID]` (where `[movieID]` is the unique identifier for each favorite movie)
  - **Remove from Favorites Button**
    - **ID:** `removeFromFavoritesButton_[movieID]` (where `[movieID]` is the unique identifier for each favorite movie)

## 4. Data Storage

The data for the Movie Recommendation System will be structured in a plain text format and stored in the local directory named `data`. Different types of data will be organized into separate text files as follows:

### a. Users Data (`users.txt`)
- **Format:** Each line contains `username,password`
- **Example:**
```
user1,secret123
user2,moviebuff
```

### b. Movie Data (`movies.txt`)
- **Format:** Each line contains `movieID,movieTitle,movieDescription,movieRating`
- **Example:**
```
1,Inception,A thief who steals corporate secrets through dreams.,8.8
2,Titanic,A love story that unfolds on the ill-fated Titanic.,7.8
```

### c. Favorites Data (`favorites.txt`)
- **Format:** Each line contains `username,movieID`
- **Example:**
```
user1,1
user1,2
```

All data files will reside in the `data` directory which should be created in the project's root folder prior to the application's execution.