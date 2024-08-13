# MailGuard

This project is a Django-based API that provides OTP (One-Time Password) authentication through email. It includes functionalities for generating and verifying OTPs, user management, and secure login/logout processes using Django Rest Framework (DRF).

## Features

- **Generate OTP**: Sends a 4-digit OTP to the user's email for authentication.
- **Verify OTP**: Verifies the OTP and generates an authentication token for the user.
- **User Management**: 
  - Admins can view, add, update, and delete users.
  - Regular users can view and update their own details.
- **Logout**: Securely logs out the user by invalidating the authentication token.

## API Endpoints

### Generate OTP

- **Endpoint**: `url/users/get-otp/`
- **Method**: POST
- **Description**: Generates a 4-digit OTP and sends it to the user's email.

### Verify OTP and Login

- **Endpoint**: `url/users/login/`
- **Method**: POST
- **Description**: Verifies the OTP and returns an authentication token.

### Logout

- **Endpoint**: `url/users/logout/`
- **Method**: POST
- **Description**: Logs out the user by deleting the authentication token.

### User Management (Admin)

- **Endpoint**: `url/users/`
  - **Method**: GET (Admin only)
  - **Description**: Retrieves a list of all active users (Admin) or the details of the current user (Regular user).

  - **Method**: POST
  - **Description**: Adds a new user.

  - **Method**: PATCH
  - **Description**: Updates user details. Admins can update any user; regular users can only update their own details.

  - **Method**: DELETE
  - **Description**: Deletes (soft delete) a user by setting `is_active` to `False`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/srikantsingh673/MailGuard
   cd MailGuard
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
