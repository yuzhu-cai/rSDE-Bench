# FitnessEquipmentRental Requirements Document

## 1. Objective
To develop a comprehensive web application for renting fitness equipment that provides users with an easy interface to browse, rent, and manage their rentals, all while using Python for development and storing data in local text files. Note that the website should start from the login page.

## 2. Language
The required development language for the FitnessEquipmentRental application is Python.

## 3. Page Design

### 3.1 Overview of Pages
This section outlines the elements that should be included on each page, along with their corresponding IDs. The web application will consist of the following 8 pages:

1. **Login Page**
   - **Page Title**: Login
   - **Content and Functionality**: Users will enter their credentials to log into the application.
   - **Element IDs**:
     - `login_form` - Form for user credentials
     - `username_field` - Input field for the username
     - `password_field` - Input field for the password
     - `login_button` - Button to submit the login form
     - `register_link` - Link to navigate to Register Page

2. **Register Page**
   - **Page Title**: Register
   - **Content and Functionality**: Users will create a new account.
   - **Element IDs**:
     - `register_form` - Form for user credentials
     - `username_field` - Input field for the username
     - `password_field` - Input field for the password
     - `name_field` - Input field for the name
     - `email_field` - Input field for the email
     - `register_button` - Button to submit the register form

3. **Homepage**
   - **Page Title**: Home
   - **Content and Functionality**: Overview of rental equipment, latest offers, and promotional banners. Links to browse equipment.
   - **Element IDs**:
     - `welcome_message` - Welcome message for users
     - `equipment_listing` - Section for displaying rental equipment
     - `promotions_section` - Area for promoting current offers
     - `browse_button` - Button to browse all equipment (navigate to Equipment Page)
     - `my_rental_button` - Button to navigate to Rental Form Page
     - `help_button` - Button to navigate to Help Page

4. **Equipment Page**
   - **Page Title**: Equipment
   - **Content and Functionality**: Detailed list of available fitness equipment with the option to rent.
   - **Element IDs**:
     - `equipment_listing` - List of all available equipment
     - `show_details_button` - Button to display details of selected equipment, and each equipment has such a button
     - `equipment_details` - Area displaying details of selected equipment
     - `rent_button` - Button to initiate the rental process for equipment displaying detailed information (navigate to Rental Form Page)

5. **Rental Form Page**
   - **Page Title**: Rental Form
   - **Content and Functionality**: A form to collect information for the rental, including rental duration and personal details.
   - **Element IDs**:
     - `rental_form` - Form for rental information
     - `equipment_id_field` - Hidden field to store the selected equipment ID
     - `rental_duration_field` - Input for rental duration
     - `user_details_field` - Input for username
     - `submit_rental_button` - Button to submit the rental request
     - `rental_confirmation_msg` - Area to show rental confirmation

6. **My Rentals Page**
   - **Page Title**: My Rentals
   - **Content and Functionality**: Users can view their current and past rentals.
   - **Element IDs**:
     - `my_current_rentals_listing` - List showing user's current rentals including rental_id,equipment_id,rental_duration,start_date
     - `return_equipment_button` - Button to navigate to Return Equipment Page
     - `my_past_rentals_listing` - List showing user's past rentals including rental_id,equipment_id,rental_duration,start_date

7. **Return Equipment Page**
   - **Page Title**: Return Equipment
   - **Content and Functionality**: A page where users can confirm the return of rented equipment.
   - **Element IDs**:
     - `return_form` - Form for return confirmation
     - `rental_id_field` - Input field for rental ID
     - `confirm_return_button` - Button to confirm the equipment return
     - `return_confirmation_msg` - Area for return confirmation message

8. **Help Page**
   - **Page Title**: Help
   - **Content and Functionality**: Users can find FAQ, contact support, and accessibility information.
   - **Element IDs**:
     - `faq_section` - Section containing frequently asked questions
     - `accessibility_info` - Section providing accessibility options

## 4. Data Storage

### 4.1 Data Format
All data for the FitnessEquipmentRental application will be stored in local text (`.txt`) files within a directory named 'data'. Each type of information will be stored in its own file.

### 4.2 Data Examples
1. **Users** (stored in `data/users.txt`):
   ```
   username,password,full_name,email
   john_doe,password123,John Doe,john@example.com
   jane_smith,password456,Jane Smith,jane@example.com
   ```

2. **Equipment** (stored in `data/equipment.txt`):
   ```
   equipment_id,name,description,availability,rental_price
   1,Treadmill,"High-quality treadmill for home use",10,15.00
   2,Dumbbells,"Set of 5kg and 10kg dumbbells",5,10.00
   ```

3. **Rentals** (stored in `data/rentals.txt`):
   ```
   rental_id,username,equipment_id,rental_duration,start_date,status
   1001,john_doe,1,7,2023-10-01,inactive
   1002,jane_smith,1,2,2023-10-09,inactive
   1003,john_doe,2,3,2023-10-09,active
   ```

4. **Returns** (stored in `data/returns.txt`):
   ```
   return_id,rental_id,date_returned
   5001,1001,2023-10-08
   5002,1002,2023-10-11
   ```

This format will aid in organizing and retrieving user, equipment, rental, and return information efficiently without the need for SQL databases.