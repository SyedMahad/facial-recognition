from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import face_recognition
from models import UserModel, user_db

# Initialize FastAPI app
app = FastAPI()

# Set up Jinja2 for rendering HTML templates
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS and JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    """
    Serve the index page.
    
    Args:
        request (Request): HTTP request object.

    Returns:
        HTMLResponse: Rendered index.html template.
    """
    # return templates.TemplateResponse("index.html", {"request": request})
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home", "show_nav": False})

@app.get("/register/", response_class=HTMLResponse)
async def serve_register(request: Request):
    """
    Serve the user registration page.
    
    Args:
        request (Request): HTTP request object.

    Returns:
        HTMLResponse: Rendered register.html template.
    """
    # return templates.TemplateResponse("register.html", {"request": request})
    return templates.TemplateResponse("register.html", {"request": request, "title": "Register", "show_nav": True})

@app.get("/sign-in/", response_class=HTMLResponse)
async def serve_sign_in(request: Request):
    """
    Serve the sign-in page.
    
    Args:
        request (Request): HTTP request object.

    Returns:
        HTMLResponse: Rendered sign-in.html template.
    """
    # return templates.TemplateResponse("sign-in.html", {"request": request})
    return templates.TemplateResponse("sign-in.html", {"request": request, "title": "Sign-In", "show_nav": True})

@app.post("/register-user/")
async def register_user(name: str = Form(...), file: UploadFile = File(...)):
    """
    Register a new user by uploading an image for facial recognition.
    
    Args:
        name (str): Name of the user to register.
        file (UploadFile): Uploaded image file containing the user's face.

    Returns:
        dict: Success message if registration is successful.

    Raises:
        HTTPException: If no face is detected or an error occurs during processing.
    """
    try:
        # Load and encode the uploaded image
        image = face_recognition.load_image_file(file.file)
        face_encodings = face_recognition.face_encodings(image)

        if not face_encodings:
            raise HTTPException(status_code=400, detail="No face found in the image")

        # Store user data
        new_user = UserModel(name=name, face_encoding=face_encodings[0].tolist())
        new_user.set_facial_encoding(face_encodings[0].tolist())
        user_db.append(new_user)

        return {"message": f"User {name} registered successfully!"}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sign-in-user/")
async def sign_in(file: UploadFile = File(...)):
    """
    Authenticate a user using facial recognition.
    
    Args:
        file (UploadFile): Uploaded image file for authentication.

    Returns:
        dict: Success message if user is authenticated.

    Raises:
        HTTPException: If authentication fails.
    """
    try:
        if not file.file:
            raise HTTPException(status_code=401, detail="No image provided")

        # Load and encode the uploaded image
        image = face_recognition.load_image_file(file.file)
        face_encodings = face_recognition.face_encodings(image)

        if not face_encodings:
            raise HTTPException(status_code=401, detail="No face detected")

        target_encoding = face_encodings[0]

        # Compare uploaded face with stored user faces
        for user in user_db:
            stored_encoding = user.get_facial_encoding()

            if stored_encoding is not None:
                match = face_recognition.compare_faces([stored_encoding], target_encoding)
                if match[0]:
                    return {"message": f"Welcome {user.name}!"}

        raise HTTPException(status_code=401, detail="No matching face found")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Face not recognized")
