# Requirements Document for OnlineThriftStore

## 1. Objective
Develop a comprehensive web application called 'OnlineThriftStore' that enables users to browse, purchase, sell, and manage second-hand items, utilizing Python for development and storing data locally in text files without the need for a SQL database.

## 2. Language and Framework
- **Development Language:** Python
- **Web Framework:** Flask

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
- **Overview:** This is the main page where users can search for items, navigate to shopping cart, checkout, sell item, user profile page.
- **Element IDs:**
  - `search_field`: Input field to search for items by their title
  - `search_button`: Button to start the search and navigate to the target item details page
  - `shopping_cart_button`: Button to navigate to the Shopping Cart page
  - `checkout_button`: Button to navigate to the checkout page
  - `sell_item_button`: Button to navigate to the sell item page
  - `user_profile_button`: Button to navigate to the user profile page

### 3.4. Item Details Page
- **Page Title:** `item_title`
- **Overview:** The title of this page is the title of the selected item (eg. if `item_title` is cell phone, the Page Title would be cell phone). This page dynamically displays detailed information for a specific item selected by the user. Each item listed for sale has a unique details page generated based on its specific data.
- **Element IDs:**
  - `item_title`: Display area for the item title
  - `item_seller`: Display area for the username of the item's seller
  - `item_price`: Display area for the item price
  - `item_status`: Display area for the item status: on_sale|sold
  - `add_to_cart_button`: Button to add the item to the shopping cart
  - `back_button`: Button to return to the Dashboard page

### 3.5. Shopping Cart Page
- **Page Title**: Shopping Cart
- **Overview**: This page shows the items added to the user's cart, allowing them to proceed to checkout or remove items.
- **Element IDs**:
  - `cart_items_list`: Container displaying all items in the cart
  - `remove_item_button`: Button to remove an item from the cart (for each item)
  - `total_price_display`: Display area for the total price of items in the cart
  - `checkout_button`: Button to proceed to the Checkout page
  - `back_button`: Button to return to the Dashboard page

### 3.6. Checkout Page
- **Page Title:** Checkout
- **Overview:** This page allows users to review their order, enter payment details, and complete the purchase.
- **Element IDs:**
  - `total_price_display`: Display area for the total price
  - `payment_method_field`: Input field to enter payment method
  - `confirm_purchase_button`: Button to confirm and finish the purchase
  - `cancel_purchase_button`: Button to cancel the purchase and return to the Shopping Cart page

### 3.7. Sell Item Page
- **Page Title**: Sell Item
- **Overview**: This page allows users to list a new item for sale by providing details such as title, description, price.
- **Element IDs**:
  - `item_title_field`: Input field for the item title
  - `item_description_field`: Input textarea for the item description
  - `item_price_field`: Input field for the item price
  - `post_item_button`: Button to post the item for sale
  - `cancel_button`: Button to discard the listing and return to the Dashboard page
  
### 3.8. User Profile Page
- **Page Title**: User Profile
- **Overview**: This page displays the user's profile information and provides options to view their listed items, order history, and account settings.
- **Element IDs**:
  - `purchased_items_display`: Display area for the list of the titles of the items purchased by user.
  - `on_sale_items_display`: Display area for the list of the titles of the items the user is currently selling
  - `logout_button`: Button to log out of the application and back to the Login Page

## 4. Data Storage

### Data Format
The application will store data in local text files located in the `data` directory. Each type of data will be saved in a separate file to organize the information efficiently.

### Data Files
- **User Data File (`users.txt`)**:
  - Format: `username:password`
  - Example:
    ```
    john_doe:abcd1234
    jane_smith:xyz9876
    ```

- **Item on sale Data File (`on_sale.txt`)**:
  - Format: `title|description|price|seller_username`
  - Example:
    ```
    cell phone|A brand new cell phone.|500.00|jane_smith
    lamp|A vintage lamp in excellent condition.|45.00|john_doe
    jacket|Stylish jacket, barely worn.|30.00|jane_smith
    ```

- **Shopping Cart Data File (`carts.txt`)**:
  - Format: `username|item_title`
  - Example:
    ```
    john_doe|cell phone
    john_doe|jacket
    ```

- **Sold items history Data File (`sold.txt`)**:
  - Format: `buyer_username|title|description|price|seller_username`
  - Example:
    ```
    john_doe|laptop|A laptop with high performance.|700.00|jane_smith
    ``` 

All text files will be created and accessed from the local `data` directory to ensure easy retrieval and management of information.


