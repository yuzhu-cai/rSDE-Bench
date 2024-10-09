# Requirements Document for GourmetFoodSubscription

## 1. Objective
Develop a comprehensive web application called 'GourmetFoodSubscription' that enables users to subscribe to gourmet food boxes, manage their subscriptions, and explore available options without the need for a SQL database, leveraging Python and storing data in local text files.

## 2. Language
The required development language for this application is Python.

## 3. Page Design

### 3.1. Login Page
- **Page Title:** Login
- **Overview:** This page allows users to log into the application with their credentials.
- **Element IDs:**
  - `username_field`: Input field for the username
  - `password_field`: Input field for the password
  - `login_button`: Button to submit login credentials
  - `error_message`: Display area for login errors
  - `register_link`: Link to the registration page

### 3.2. Registration Page
- **Page Title:** Register
- **Overview:** This page allows new users to create an account.
- **Element IDs:**
  - `register_username_field`: Input field for the new username
  - `register_password_field`: Input field for the new password
  - `confirm_password_field`: Input field for confirming the password
  - `register_button`: Button to submit registration details
  - `registration_success_message`: Display area for registration confirmations or errors

### 3.3. Dashboard Page
- **Page Title:** Dashboard
- **Overview:** This is the main page that displays the user's current subscriptions and provides options to manage them.
- **Element IDs:**
  - `subscription_list`: Container to display all active subscriptions
  - `add_subscription_button`: Button to navigate to the Add Subscription Page
  - `view_subscription_button`: Button to navigate to the View Subscription Page
  - `contact_us_button`: Button to navigate to the Contact Us Page
  - `logout_button`: Button to log out of the application

### 3.4. Add Subscription Page
- **Page Title:** Add Subscription
- **Overview:** This page allows users to subscribe to a new gourmet food box by entering the type, frequency, and start date.
- **Element IDs:**
  - `subscription_type_field`: Input field for the subscription type
  - `subscription_frequency_field`: Input field for the frequency (e.g., Weekly, Monthly)
  - `subscription_start_date_field`: Input field for the subscription start date
  - `save_subscription_button`: Button to save the new subscription and return to the dashboard
  - `cancel_button`: Button to discard changes and return to the dashboard

### 3.5. View Subscription Page
- **Page Title**: View Subscription
- **Overview**: This page displays the details of subscriptions, allowing users to view or cancel them.
- **Element IDs**:
  - `subscription_type_display`: Display area for the list of subscription types
  - `subscription_frequency_display`: Display area for the list of subscription frequency
  - `subscription_start_date_display`: Display area for the list of subscription start dates
  - `subscription_type_field`: Input field for the subscription type
  - `edit_subscription_button`: Button to navigate to the Edit Subscription Page with pre-filled data, to edit the subscription whose type is same as that entered in `subscription_type_field`
  - `delete_subscription_button`: Button to delete the subscription whose type is same as that entered in `subscription_type_field`
  - `back_button`: Button to return to the Dashboard page

### 3.6. Edit Subscription Page
- **Page Title**: Edit Subscription
- **Overview**: This page displays detailed information about a specific subscription selected by the user with pre-filled information about the subscription. This page allows users to edit the information of this subscription.
- **Element IDs**:
  - `subscription_type_field`: Input field for the subscription type with pre-filled subscription type
  - `subscription_frequency_field`: Input field for the frequency with pre-filled subscription frequency
  - `subscription_start_date_field`: Input field for the subscription start date with pre-filled subscription start date
  - `save_subscription_button`: Button to save change to the subscription and return to the dashboard
  - `cancel_button`: Button to discard changes and return to the dashboard

### 3.7. Contact Us Page
- **Page Title:** Contact Us
- **Overview:** This page allows users to send inquiries or feedback to customer support.
- **Element IDs:**
  - `contact_name_field`: Input field for the user's name
  - `contact_email_field`: Input field for the user's email
  - `contact_message_field`: Input textarea for the user's message
  - `send_message_button`: Button to submit the message
  - `back_button`: Button to return to the Dashboard page

## 4. Data Storage

### Data Format
The application will store data in local text files located in the `data` directory. Each type of data will be saved in a separate file to organize the information efficiently.

### Data Files
- **User Data File (`users.txt`)**:
  - Format: `username:hashed_password`
  - Example:
    ```
    john_doe:abcd1234hashed
    jane_smith:xyz9876hashed
    ```

- **Subscription Data File (`subscriptions.txt`)**:
  - Format: `subscription_id|username|type|frequency|start_date`
  - Example:
    ```
    1|john_doe|Vegan|Monthly|2024-09-01
    2|jane_smith|Meat Lovers|Weekly|2024-08-30
    ```

- **Food Box Data File (`food_boxes.txt`)**:
  - Format: `box_id|name|description`
  - Example:
    ```
    1|Vegan|A selection of fresh vegan ingredients and recipes.
    2|Meat Lovers|Premium cuts of meat with seasoning and cooking tips.
    3|Cheese King|All kinds of food with cheese.
    ```

- **Contact Us Data File (`inquiries.txt`)**:
  - Format: `inquiry_id|username|email|message`
  - Example:
    ```
    1|jane_smith|js@food.com|Unable to login.
    ```

All text files will be created and accessed from the local `data` directory to ensure easy retrieval and management of information.