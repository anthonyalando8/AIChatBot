$(document).ready(function(){
    //Login js
    $("#login-form").submit(function(event){
        event.preventDefault();
        const loginBtn = document.getElementById("login-btn");
        // const loginSpinner = document.getElementById("login-spinner");

        const email = document.getElementById("login-email").value.trim();
        const password = document.getElementById("login-password").value.trim();
        if (!email || !password) {
            alert("All fields are required.");
            return;
        }
        loginBtn.setAttribute("disabled", "disabled");
        // loginSpinner.style.display = "block";
        loginBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        const formData = new FormData(this);
        fetch("/login/", {
            method:'POST',
            body: formData
        }).then(response=>{
            return response.json();
        }).then(data=>{
            const message = data.message;
            const status = data.status;
            
            if(status == 200){
                window.location.href = "/";
            }else{
                alert(message);
            }
        }).catch(error=>{
            alert("Something went wrong");
        }).finally(()=>{
            loginBtn.innerHTML = "Login";
            loginBtn.removeAttribute("disabled");
        
            // loginSpinner.style.display = "none";
        });
    });

    // sign up js
    $("#signup-form").submit(function(event){
        event.preventDefault();
        const signupBtn = document.getElementById("signup-btn");
        // const signupSpinner = document.getElementById("signup-spinner");

        const firstName = document.getElementById("signup-first-name").value.trim();
        const lastName = document.getElementById("signup-last-name").value.trim();
        const email = document.getElementById("signup-email").value.trim();
        const password = document.getElementById("signup-password").value.trim();
        
        if (!firstName || !lastName || !email || !password) {
            alert("All fields are required.");
            return;
        }
        signupBtn.setAttribute("disabled", "disabled");
        signupBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        // signupSpinner.style.display = "block";
        const formData = new FormData(this);
        fetch("/signup/", {
            method:'POST',
            body: formData
        }).then(response=>{
            return response.json();
        }).then(data=>{
            const message = data.message;
            const status = data.status;
            if(status == 200){
                window.location.href = "/login/";
            }else{
                alert(message);
            }
        }).catch(error=>{
            alert("Error"+error);
        }).finally(()=>{
            signupBtn.innerHTML = "Sign up"
            signupBtn.removeAttribute("disabled");
        
            // signupSpinner.style.display = "none";
        });
    });
    
});
