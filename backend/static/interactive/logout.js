document
  .getElementById("logout-link")
  .addEventListener("click", function (event) {
    // event.preventDefault();
    console.log("Log out ");
    if (confirm("Are you sure you want to log out?")) {
        console.log("Confirm");
        // Send POST request to /logout endpoint
        fetch("/logout", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ logout: true })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Log out was successful, redirect to login page
            window.location.href = "/login";
          } else {
            // Handle error
            console.error(data.error);
          }
        })
        .catch(error => console.error(error));
      }      
  });
