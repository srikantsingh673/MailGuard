**MailGuard**

This project is a Django-based API that provides OTP (One-Time Password) authentication through
email. It includes functionalities for generating and verifying OTPs, user management, and secure
login/logout processes using Django Rest Framework (DRF).

Features:
- Generate OTP: Sends a 4-digit OTP to the user's email for authentication.
- Verify OTP: Verifies the OTP and generates an authentication token for the user.
- User Management: Admins can view, add, update, and delete users. Regular users can view and
update their own details.
- Logout: Securely logs out the user by invalidating the authentication token.
- 
API Endpoints:
1. Generate OTP
- Endpoint: url/users/get-otp/
- Method: POST
- Description: Generates a 4-digit OTP and sends it to the user's email.
- Request Body:
 {
 "email": "user@example.com"
 }
- Response:
 {
 "message": "OTP sent to email."
 }

2. Verify OTP and Login
- Endpoint: url/users/login/
- Method: POST
- Description: Verifies the OTP and returns an authentication token.
- Request Body:
 {
 "email": "user@example.com",
 "otp": "1234"
 }
- Response:
 {
 "token": "your-auth-token"
 }

3. Logout
- Endpoint: url/users/logout/
- Method: POST
- Description: Logs out the user by deleting the authentication token.
- Response:
 {
 "detail": "Successfully logged out."
 }

4. User Management (Admin)
- Endpoint: url/users/
  
- Method: GET (Admin only)
- Description: Retrieves a list of all active users (Admin) or the details of the current user (Regular
user).
- Response:
 {
 "data": [ ...user_details... ],
 "message": "Data retrieved successfully"
 }

- Method: POST
- Description: Adds a new user.
- Request Body:
 {
 "email": "newuser@example.com",
 "full_name": "New User",
 "mobile": "1234567890"
 }
- Response:
 {
 "data": [ ...new_user_details... ],
 "message": "User added successfully"
 }

- Method: PATCH
- Description: Updates user details. Admins can update any user; regular users can only update
their own details.
- Request Body:
 {
 "id": "user_id",
 "field_to_update": "new_value"
 }
- Response:
 {
 "data": [ ...updated_user_details... ],
 "message": "Details updated successfully."
 }

-  Method: DELETE
- Description: Deletes (soft delete) a user by setting is_active to False.
- Request Body:
 {
 "id": "user_id"
 }
- Response:
 {
 "data": [ ...deleted_user_details... ],
 "message": "User deleted successfully"
 }

Installation:
1. Clone the repository:
2. Install dependencies:
 pip install -r requirements.txt
3. Run migrations:
 python manage.py migrate
4. Run the development server:
 python manage.py runserver

Environment Variables:
Make sure to set the following environment variables:
- SECRET_KEY - Django's secret key.
- EMAIL_HOST - SMTP server for sending emails.
- EMAIL_PORT - Port for the SMTP server.
- EMAIL_HOST_USER - SMTP server username.
- EMAIL_HOST_PASSWORD - SMTP server password.
- EMAIL_USE_TLS or EMAIL_USE_SSL - Whether to use TLS/SSL.

Contact:
For any questions or suggestions, please feel free to contact srikantsingh673@gmail.com.
