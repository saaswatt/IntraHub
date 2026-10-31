
document.addEventListener("DOMContentLoaded", () => {

    // Password visibility toggle
    const passwordInput = document.getElementById("password");
    const togglePassword = document.getElementById("toggle-password");

    if (passwordInput && togglePassword) {

        togglePassword.addEventListener("click", () => {

            const isPassword =
                passwordInput.type === "password";

            passwordInput.type =
                isPassword ? "text" : "password";

            togglePassword.textContent =
                isPassword ? "Hide" : "Show";

            togglePassword.setAttribute(
                "aria-label",
                isPassword ? "Hide password" : "Show password"
            );

        });

    }

    // Login button loading state
    const loginForm = document.getElementById("login-form");
    const connectButton = document.getElementById("connect-button");
    const buttonText = document.getElementById("button-text");

    if (loginForm && connectButton) {

        loginForm.addEventListener("submit", () => {

            connectButton.disabled = true;

            if (buttonText) {
                buttonText.textContent = "Authenticating...";
            }

        });

    }

});
