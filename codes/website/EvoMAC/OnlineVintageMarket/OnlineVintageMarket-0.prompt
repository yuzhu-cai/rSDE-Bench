# Requirement Document for OnlineVintageMarket

## 1. Objective
The task is to develop a comprehensive web application, 'OnlineVintageMarket', for buying and selling vintage items that utilizes Python and stores information in local text files, eliminating the need for SQL databases. Note that the website should start from the login page.

## 2. Language
The required development language for this task is Python.

## 3. Page Design

### 3.1 Login Page
- **Title:** Login
- **ID List:**
  - `login-form` (ID for the form)
  - `username` (ID for username input field)
  - `password` (ID for password input field)
  - `login-button` (ID for login button)
  
#### Overview
This page allows users to log in to their accounts. If the user has forgotten their password, they can click on the "Forgot Password" link.

### 3.2 Home Page
- **Title:** Home
- **ID List:**
  - `header` (ID for header section)
  - `item-list` (ID for displaying vintage items)
  - `create-listing-button` (ID for button to navigate to Listing Page)
  - `search-field` (ID for inputing item name to search the item)
  - `search-button` (ID for search button)
  - `search-result` (ID for displaying the searched item's name, description and price)
  - `item-details-button` (ID for button: each item has such a button that navigates to Item Details Page, displaying its specific information)
  
#### Overview
The homepage features a list of available vintage items, a search bar to find specific items, and options to filter by category. A prominent button allows users to create a new listing.

### 3.3 Listing Page
- **Title:** Create Listing
- **ID List:**
  - `listing-form` (ID for the form)
  - `item-name` (ID for item name input field)
  - `item-description` (ID for item description input field)
  - `item-price` (ID for item price input field)
  - `submit-listing-button` (ID for button to submit a listing)
  
#### Overview
On this page, users can create a new listing for a vintage item. Users will enter the item's name, description, and price.

### 3.4 Item Details Page
- **Title:** Item Details
- **ID List:**
  - `item-title` (ID for displaying the item's title)
  - `item-description` (ID for displaying the item's description)
  - `item-price` (ID for displaying the item's price)
  - `back-button` (ID for going back to the Home Page)
  
#### Overview
This page displays detailed information about a specific vintage item. Users can view the item title, description, and price, with an option to return to the homepage.

## 4. Data Storage

### Data Format
Data will be stored in plain text files located within the 'data' directory. Each type of data will have its own file:

1. **Users Data**
   - **File Name:** `users.txt`
   - **Data Format:** Each line represents a user in the format:
     ```
     username,password
     ```
   - **Example Data:**
     ```
     johndoe,password123
     janedoe,qwerty456
     ```

2. **Listings Data**
   - **File Name:** `listings.txt`
   - **Data Format:** Each line represents a listing in the format:
     ```
     item_name,item_description,item_price
     ```
   - **Example Data:**
     ```
     Vintage Clock,Old mechanical clock from the 1960s,25.00
     Retro Vinyl Record,Classic rock album from the 70s,15.00
     ```

### Directory Structure
```
/OnlineVintageMarket
    └── /data
        ├── users.txt
        └── listings.txt
```

This requirements document outlines the foundational aspects necessary for the development and functionality of the OnlineVintageMarket application, ensuring clarity in objectives, languages, page designs, and data storage needs.