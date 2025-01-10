from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import face_recognition

from models import UserModel, user_db


app = FastAPI()

# Set up Jinja2 for HTML templates
templates = Jinja2Templates(directory="templates")


@app.post("/register-user/")
async def register_user(name: str = Form(...), file: UploadFile = File(...)):
    """
    Register a new user by providing a name and an image file for facial recognition.

    Args:
        name (str): The name of the user to be registered.
        file (UploadFile): The image file containing the user's face.

    Returns:
        dict: A success message if registration is successful, or an error if not.

    Raises:
        HTTPException: If no face is found or other errors occur during processing.
    """
    try:
        # Load the image file and extract face encodings
        image = face_recognition.load_image_file(file.file)
        face_encodings = face_recognition.face_encodings(image)

        # If no face is found, raise an error
        if len(face_encodings) == 0:
            raise HTTPException(status_code=400, detail="No face found in the image")

        # Create a new UserModel and store the face encoding
        new_user = UserModel(name=name, face_encoding=face_encodings[0].tolist())
        new_user.set_facial_encoding(face_encodings[0].tolist())  # Convert numpy array to list for JSON serialization
        user_db.append(new_user)  # Append the new user to the in-memory database

        return {"message": f"User {name} registered successfully!"}

    except Exception as e:
        # Catch and raise an error with appropriate details if something goes wrong
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# Sign-in endpoint using facial recognition
@app.post("/sign-in-user/")
async def sign_in(file: UploadFile = File(...)):
    """
    Sign in a user by comparing the provided image file with the stored facial encodings.

    Args:
        file (UploadFile): The image file containing the user's face.

    Returns:
        dict: A success message with the user's name if authentication is successful, or an error if not.

    Raises:
        HTTPException: If no image is provided, no face is detected, or no matching face is found.
    """
    try:
        # Ensure that an image file has been uploaded
        if not file.file:
            raise HTTPException(status_code=401, detail="No image provided")

        # Load the image and extract face encodings
        image = face_recognition.load_image_file(file.file)
        face_encodings = face_recognition.face_encodings(image)

        # If no face is found, raise an error
        if len(face_encodings) == 0:
            raise HTTPException(status_code=401, detail="No face detected")

        # Use the first face encoding in the image
        target_encoding = face_encodings[0]

        # Compare the target face encoding with all stored face encodings in the database
        for user in user_db:
            stored_encoding = user.get_facial_encoding()

            if stored_encoding is not None:
                # Compare the stored encoding with the target encoding
                match_result = face_recognition.compare_faces([stored_encoding], target_encoding)

                if match_result[0]:  # If a match is found
                    return {"message": f"Welcome {user.name}!"}

        # Raise an error if no match is found
        raise HTTPException(status_code=401, detail="No matching face found")

    except Exception as e:
        print(e)
        # Catch and raise an error with appropriate details if something goes wrong
        raise HTTPException(status_code=401, detail="Face not recognized")


# Root route to serve the index.html template
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serve the root HTML page (index.html) for the application.

    Args:
        request (Request): The HTTP request object.

    Returns:
        HTMLResponse: The rendered index.html template.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serve the root HTML page (index.html) for the application.

    Args:
        request (Request): The HTTP request object.

    Returns:
        HTMLResponse: The rendered index.html template.
    """
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/sign-in/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serve the root HTML page (index.html) for the application.

    Args:
        request (Request): The HTTP request object.

    Returns:
        HTMLResponse: The rendered index.html template.
    """
    return templates.TemplateResponse("sign-in.html", {"request": request})
