$(document).ready(function () {
  $("#loginForm").on("submit", function (e) {
    e.preventDefault();

    var username = $("#username").val();
    var password = $("#password").val();

    $.ajax({
      url: "http://localhost:8000/api/token/",
      method: "POST",
      data: JSON.stringify({
        username: username,
        password: password,
      }),
      contentType: "application/json",
      success: function (response) {
        // Store tokens
        localStorage.setItem("access", response.access);
        localStorage.setItem("refresh", response.refresh);

        // Redirect to user's page
        window.location.href = "users.html";
      },
      error: function (error) {
        ajaxErrorHandler(error, "An error occurred while logging in.");
      },
    });
  });
});
