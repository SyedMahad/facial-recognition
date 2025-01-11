/**
 * Set the loading state for buttons during form submission.
 * @param {HTMLElement} button - The button element.
 * @param {boolean} isLoading - Whether to show loading state.
 */
function setLoadingState(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.setAttribute('data-original-text', button.innerText);
        button.innerHTML = 'Loading <span class="loader"></span>';
    } else {
        button.disabled = false;
        button.innerText = button.getAttribute('data-original-text');
    }
}

/**
 * Display a message on the UI.
 * @param {string} message - The message text.
 * @param {string} type - 'success' or 'error'.
 */
function displayMessage(message, type) {
    const messageBox = document.getElementById("message-box");
    messageBox.innerText = message;
    messageBox.className = `message ${type}`;
}

/**
 * Handle user registration.
 */
async function registerUser() {
    const formData = new FormData();
    const nameInput = document.getElementById("name").value;
    const fileInput = document.getElementById("file").files[0];
    const registerBtn = document.getElementById("register-btn");
    const signInBtn = document.getElementById("sign-in-btn");

    if (!nameInput || !fileInput) {
        displayMessage("Please enter your name and select an image.", "error");
        return;
    }

    formData.append("name", nameInput);
    formData.append("file", fileInput);

    setLoadingState(registerBtn, true);

    try {
        const response = await fetch("/register-user/", { method: "POST", body: formData });
        const data = await response.json();
        displayMessage(response.ok ? data.message : data.detail || "Registration failed.", response.ok ? "success" : "error");
        registerBtn.style.display = "none";
        signInBtn.style.display = "block";
    } catch {
        displayMessage("An error occurred during registration.", "error");
    } finally {
        setLoadingState(registerBtn, false);
    }
}

/**
 * Handle user sign-in.
 */
async function signInUser() {
    const formData = new FormData();
    const fileInput = document.getElementById("signin-file").files[0];
    const signInBtn = document.getElementById("signin-btn");

    if (!fileInput) {
        displayMessage("Please upload an image for sign-in.", "error");
        return;
    }

    formData.append("file", fileInput);
    setLoadingState(signInBtn, true);

    try {
        const response = await fetch("/sign-in-user/", { method: "POST", body: formData });
        const data = await response.json();
        displayMessage(response.ok ? data.message : data.detail || "Sign-in failed.", response.ok ? "success" : "error");
    } catch {
        displayMessage("An error occurred during sign-in.", "error");
    } finally {
        setLoadingState(signInBtn, false);
    }
}


/**
 * Handle user redirection to sign-in page.
 */
async function redirectToSignIn(event) {
    event.preventDefault();  // Prevent form submission
    window.location.href = "/sign-in/";
}
