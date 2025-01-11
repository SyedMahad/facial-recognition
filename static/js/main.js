// Real-time input validation for name
const nameInput = document.getElementById("name");
if (nameInput) {
    nameInput.addEventListener("focusout", function() {
        if (this.value.trim() === "") {
            displayMessage("Name cannot be empty.", "error");
        } else {
            displayMessage("", "");
        }
    });
}

// Real-time input validation for image upload
const fileInput = document.getElementById("file");
if (fileInput) {
    fileInput.addEventListener("cancel", function() {
        if (this.files.length === 0) {
            displayMessage("Please upload an image.", "error");
        } else {
            displayMessage("", "");
        }
    });
}

// Real-time input validation for image upload
const fileSignInInput = document.getElementById("signin-file");
if (fileSignInInput) {
    fileSignInInput.addEventListener("cancel", function() {
        if (this.files.length === 0) {
            displayMessage("Please upload an image.", "error");
        } else {
            displayMessage("", "");
        }
    });
}

function showToast(message, type) {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("show");
    }, 100);

    setTimeout(() => {
        toast.classList.remove("show");
        toast.remove();
    }, 3000);
}

// Highlight active link
const navLinks = document.querySelectorAll(".nav-item");
navLinks.forEach(link => {
    if (window.location.pathname === link.getAttribute("href")) {
        link.classList.add("active-nav");
    }
});

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
 * Handle user registration.
 */
async function registerUser() {
    const formData = new FormData();
    const nameInput = document.getElementById("name").value;
    const fileInput = document.getElementById("file").files[0];
    const registerBtn = document.getElementById("register-btn");
    const signInBtn = document.getElementById("sign-in-btn");

    if (!nameInput || !fileInput) {
        showToast("Please enter your name and select an image.", "error");
        return;
    }

    formData.append("name", nameInput);
    formData.append("file", fileInput);

    setLoadingState(registerBtn, true);

    try {
        const response = await fetch("/register-user/", { method: "POST", body: formData });
        const data = await response.json();
        showToast(response.ok ? data.message : data.detail || "Registration failed.", response.ok ? "success" : "error");
        registerBtn.style.display = "none";
        signInBtn.style.display = "flex";
    } catch {
        showToast("An error occurred during registration.", "error");
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
        showToast("Please upload an image for sign-in.", "error");
        return;
    }

    formData.append("file", fileInput);
    setLoadingState(signInBtn, true);

    try {
        const response = await fetch("/sign-in-user/", { method: "POST", body: formData });
        const data = await response.json();
        showToast(response.ok ? data.message : data.detail || "Sign-in failed.", response.ok ? "success" : "error");
    } catch {
        showToast("An error occurred during sign-in.", "error");
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
