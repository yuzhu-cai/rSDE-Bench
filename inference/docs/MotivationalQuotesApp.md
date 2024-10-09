# Requirements Document for MotivationalQuotesApp

## 1. Objective
Develop a comprehensive web application named "MotivationalQuotesApp" to provide users with a collection of motivational quotes, allowing them to view, add, and manage their favorite quotes effectively.

## 2. Language
Python is the required development language for the development of the MotivationalQuotesApp.

## 3. Page Design

### 1. Login Page
- **Page Title:** Login
- **Page ID:** login_page
- **Content & Functionality:**
    - Username Input Field:
      - **ID:** username_input
      - **Type:** Text
    - Password Input Field:
      - **ID:** password_input
      - **Type:** Password
    - Login Button:
      - **ID:** login_button
      - **Function:** Validates user credentials and redirects to the home page if successful.
    - About Button:
      - **ID:** about_button
      - **Function:** Redirects to the About page.

### 2. Home Page
- **Page Title:** Home
- **Page ID:** home_page
- **Content & Functionality:**
    - Welcome Message:
      - **ID:** welcome_message
    - Display Quotes Section:
      - **ID:** quotes_display
      - **Function:** Lists all motivational quotes with options to edit or delete each quote.
      - **Quote Item:**
        - **ID:** quote_item_[quote_id] (where `[quote_id]` is a unique identifier for each quote stating from 0)
        - **Edit Button:**
          - **ID:** edit_quote_[quote_id] (where `[quote_id]` corresponds to the specific quote being edited)
        - **Delete Button:**
          - **ID:** delete_quote_[quote_id] (where `[quote_id]` corresponds to the specific quote being deleted)
    - Add Quote Button:
      - **ID:** add_quote_button
      - **Function:** Redirects to the Add Quote page.
    - Favorites Button:
      - **ID:** favorites_button
      - **Function:** Redirects to the Favorites page.

### 3. Add Quote Page
- **Page Title:** Add Quote
- **Page ID:** add_quote_page
- **Content & Functionality:**
    - Quote Input Field:
      - **ID:** quote_input
      - **Type:** Textarea
    - Author Input Field:
      - **ID:** author_input
      - **Type:** Text
    - Submit Quote Button:
      - **ID:** submit_quote_button
      - **Function:** Validates the input and saves the quote to storage.

### 4. Edit Quote Page
- **Page Title:** Edit Quote
- **Page ID:** edit_quote_page
- **Content & Functionality:**
    - Quote Input Field:
      - **ID:** edit_quote_input
      - **Type:** Textarea
    - Author Input Field:
      - **ID:** edit_author_input
      - **Type:** Text
    - Update Quote Button:
      - **ID:** update_quote_button
      - **Function:** Validates the input and updates the existing quote.

### 5. Delete Quote Confirmation Page
- **Page Title:** Delete Confirmation
- **Page ID:** delete_confirmation_page
- **Content & Functionality:**
    - Confirmation Message:
      - **ID:** confirm_message
    - Confirm Deletion Button:
      - **ID:** confirm_deletion_button
      - **Function:** Deletes the selected quote and redirects back to the home page.
    - Cancel Button:
      - **ID:** cancel_button
      - **Function:** Redirects back to the home page without deletion.

### 6. Favorites Page
- **Page Title:** Favorites
- **Page ID:** favorites_page
- **Content & Functionality:** 
    - Display Favorite Quotes Section:
      - **ID:** favorites_display
      - **Function:** Lists all quotes marked as favorites.


### 7. About Page
- **Page Title:** About
- **Page ID:** about_page
- **Content & Functionality:**
    - Application Description:
      - **ID:** app_description
    - Developer Information:
      - **ID:** developer_info

## 4. Data Storage

### Data Format
Data will be stored in plain text format (.txt) within the directory named 'data'. Different types of data will be stored in separate files. 

### Data Files
1. **Quotes.txt**
   - **Content Format:** 
     ```
     Quote|Author
     ```
   - **Data Example:**
     ```
     The only way to do great work is to love what you do.|Steve Jobs
     Success is not the key to happiness. Happiness is the key to success.|Albert Schweitzer
     ```

2. **Users.txt**
   - **Content Format:** 
     ```
     Username|Password
     ```
   - **Data Example:**
     ```
     user1|abc123
     user2|def456
     ```

3. **Favorites.txt**
   - **Content Format:** 
     ```
     Username|Quote|Author
     ```
   - **Data Example:**
     ```
     user1|The best way to predict the future is to invent it.|Alan Kay
     ```

By adhering to this requirements document, the development team will ensure a robust and user-friendly MotivationalQuotesApp.