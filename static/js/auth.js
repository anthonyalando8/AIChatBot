document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("signup-form");
  const btn = document.getElementById("signup-btn");
  const spinner = document.getElementById("signup-spinner");

  form.addEventListener("submit", async function (event) {
      event.preventDefault();

      // Get form values
      const firstName = document.getElementById("signup-first-name").value.trim();
      const lastName = document.getElementById("signup-last-name").value.trim();
      const email = document.getElementById("signup-email").value.trim();
      const password = document.getElementById("signup-password").value.trim();

      // Validate inputs
      if (!firstName || !lastName || !email || !password) {
          createToast("All fields are required.", "error");
          return;
      }

      // Show loading spinner
      btn.disabled = true;
      spinner.classList.remove("hidden");

      try {
          const response = await fetch("/signup/", {
              method: "POST",
              headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
              body: JSON.stringify({ first_name: firstName, last_name: lastName, email, password }),
          });

          const data = await response.json();

          if (response.status === 201) {
              createToast("User created successfully!", "success");
              setTimeout(() => window.location.href = "/login/", 2000);
          } else {
              createToast(data.error || "Signup failed. Try again.", "error");
          }
      } catch (error) {
          createToast("Network error. Please try again.", "error");
      } finally {
          btn.disabled = false;
          spinner.classList.add("hidden");
      }
  });
});

// Function to get CSRF token
function getCSRFToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

// Function to show toast notifications
function createToast(message, status) {
  alert(`${status.toUpperCase()}: ${message}`); // Replace with a fancier toast UI
}
