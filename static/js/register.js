document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent default form submission

    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirm_password").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    alert("Registration Successful!");
    // Here, you can send data to the backend using Fetch API
});
