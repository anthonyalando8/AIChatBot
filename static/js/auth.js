document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("signup-form");
  const btn = document.getElementById("signup-btn");

  form.addEventListener("submit", async function (event) {
      event.preventDefault();

      const firstName = document.getElementById("signup-first-name").value.trim();
      const lastName = document.getElementById("signup-last-name").value.trim();
      const email = document.getElementById("signup-email").value.trim();
      const password = document.getElementById("signup-password").value.trim();

      if (!firstName || !lastName || !email || !password) {
          createToast("All fields are required.", "error");
          return;
      }

      btn.disabled = true;

      try {
          const response = await fetch("/signup/", {
              method: "POST",
              headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
              body: JSON.stringify({ first_name: firstName, last_name: lastName, email, password }),
          });

          const data = await response.json();

          if (response.ok) {
              createToast(data.message, "success");
              setTimeout(() => window.location.href = "/login/", 2000);
          } else {
              createToast(data.error || "Signup failed. Try again.", "error");
          }
      } catch (error) {
          createToast("Network error. Please try again.", "error");
      } finally {
          btn.disabled = false;
      }
  });
});

// Function to get CSRF token
function getCSRFToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

// Function to show toast notifications
function createToast(message, status) {
  alert(`${status.toUpperCase()}: ${message}`);  // Replace with a toast library if needed
}

//Login js

document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("login-form");
  const loginBtn = document.getElementById("login-btn");
  const loginSpinner = document.getElementById("login-spinner");

  loginForm.addEventListener("submit", async function (event) {
      event.preventDefault();

      const email = document.getElementById("login-email").value.trim();
      const password = document.getElementById("login-password").value.trim();

      if (!email || !password) {
          createToast("All fields are required.", "error");
          return;
      }

      loginBtn.disabled = true;
      loginSpinner.style.display = "block";

      const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

      try {
          const response = await fetch(loginForm.action, {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": csrfToken
              },
              body: JSON.stringify({ email, password })
          });

          const data = await response.json();

          if (response.status === 200) {
              createToast("Logged in successfully!", "success");
              setTimeout(() => window.location.href = "/", 1000); // Redirect to home
          } else if (response.status === 401) {
              createToast("Invalid credentials.", "warning");
          } else {
              createToast("An error occurred. Please try again.", "error");
          }
      } catch (error) {
          createToast("Server error. Try again later.", "error");
      } finally {
          loginBtn.disabled = false;
          loginSpinner.style.display = "none";
      }
  });
});
