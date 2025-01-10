# Facial Recognition Authentication System

This project is a facial recognition-based authentication system built using FastAPI and the `face_recognition` library. It allows users to register their face using an image and then sign in using facial recognition. This project serves as a **Proof of Concept (POC)** to demonstrate the basic functionality of facial recognition for authentication purposes. User data is stored in an in-memory database (for demo purposes), but this can be extended to a real database in production environments.


## Features

- **Register**: Users can register by uploading an image containing their face and providing a name.
- **Sign-In**: Users can sign in by uploading an image. The system checks if the face matches any registered users.
- **Facial Recognition**: Powered by `dlib` through the `face_recognition` Python library, which provides high-accuracy face detection and encoding comparison.
- **In-Memory Database**: For simplicity, the project stores user face encodings in an in-memory list (`user_db`). In production, this should be replaced with a persistent database.
- **HTML Templating**: The app serves a basic HTML page for user interaction, created with Jinja2 templates.

## Project Structure

```
facial-recognition-app/ 
│ 
├── app.py # Main FastAPI application logic
├── models.py # UserModel class and in-memory database
├── templates/
│   └── index.html # Basic HTML form for user registration and sign-in
└── README.md # Project documentation
```

## Installation

### Prerequisites

- **Python 3.7+**
- **pip** (Python package manager)
- **virtualenv** (optional, but recommended for isolating dependencies)

### Steps

1. Clone the repository:

   ```bash
   git clone git@github.com:Diya-Interactive/facial-recognition.git
   cd facial-recognition-app

1. Set up a virtual environment (optional, but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # For Linux/MacOS
    venv\Scripts\activate      # For Windows
    ```

1. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    The key dependencies are:

    - `fastapi`
    - `uvicorn`
    - `face_recognition`
    - `jinja2`

1. Run the application:
    ```bash
    uvicorn app:app --reload
    ```
1. Visit the application in your browser at http://127.0.0.1:8000/.

## API Endpoints

### 1. Register User

- **Endpoint:** /register/
- **Method:** POST
- **Description:** Registers a new user by uploading an image and providing a name. The user's facial encoding is extracted and stored.

#### Form Data:

- **name:** Name of the user (string)
- **file:** Image file containing the user's face (image/*)

#### Response:

- **200 OK:** Returns a success message if the user is registered successfully.
- **400 Bad Request:** If no face is found in the image.
- **500 Internal Server Error:** For any server-side errors.

### 2. Sign In

- **Endpoint:** /sign-in/
- **Method:** POST
- **Description:** Authenticates a user by comparing the uploaded image with stored facial encodings.

#### Form Data:

- **file:** Image file containing the user's face (image/*)

#### Response:

- **200 OK:** Returns a success message with the user’s name if a match is found.
- **401 Unauthorized:** If no match is found or no face is detected in the image.


### 3. Home Page

- **Endpoint:** /
- **Method:** GET
- **Description:** Serves the root HTML page (index.html), where users can register and sign in through forms.

## Current Issue

The following test case outlines a potential issue with facial recognition when attempting to use an image of an image.

### Test Steps:

1. **Step #01:** Take a selfie from your phone and use that image to register in the system.
1. **Step #02:** Take a picture of this selfie from another phone (i.e., a photo of the registered selfie) and try to use that image for signing in.

### Expected Outcome:

- The system should reject the attempt to sign in because the new image (a photo of the selfie) should not perfectly match the original encoding.

### Current Outcome:

- The system accepts the sign-in attempt, allowing users to sign in with a picture of the registered selfie.

## Code Overview

### `models.py`

- **UserModel:** Represents a user, including their name and facial encoding. The encoding is stored as binary data for efficient storage and retrieval.
- **user_db:** An in-memory list that acts as the database for registered users.

### app.py

- `/register/`: Registers a new user by extracting their facial encoding from the uploaded image and storing it.
- `/sign-in/`: Authenticates a user by comparing the uploaded face image with the registered face encodings.
- `/`: Serves the root HTML page for the application.

### index.html

A simple HTML page with forms for user registration and sign-in. The forms accept an image file and (for registration) the user’s name.

## Notes

- This is a demo application that stores user data in memory. For production use, integrate a persistent database (e.g., PostgreSQL, SQLite).
- Ensure that the application runs in a secure environment when deployed to production, as it deals with personal biometric data (faces).

