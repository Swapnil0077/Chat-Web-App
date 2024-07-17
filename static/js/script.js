function validateForm() {
    var username = document.getElementById("username").value.trim();
    var password = document.getElementById("password").value.trim();

    if (username === "") {
        alert("Please enter your username.");
        return false;
    }

    if (password === "") {
        alert("Please enter your password.");
        return false;
    }

    // Simulate authentication process (replace with actual backend logic)
    if (username === "demo" && password === "demo123") {
        alert("Login successful!");
        return true;
    } else {
        alert("Invalid username or password. Please try again.");
        return false;
    }
}
