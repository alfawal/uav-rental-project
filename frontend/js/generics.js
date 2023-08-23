function getAccessToken() {
  // Get the access token from the local storage
  // If it doesn't exist, redirect to the login page
  const accessToken = localStorage.getItem("access");
  if (!accessToken) {
    window.location.href = "login.html";
    return;
  }
  return accessToken;
}

function dataTableQueryParamsHandler(data) {
  return {
    page: data.start / data.length + 1,
    page_size: data.length,
    ordering:
      data.order[0].dir === "asc"
        ? data.columns[data.order[0].column].data
        : "-" + data.columns[data.order[0].column].data,
    search: data.search.value,
  };
}

function ajaxErrorHandler(error, optionalMessage) {
  // If the error is 401 and the refresh token is available, try to refresh
  // the access token
  let canRequestAgain = false;
  if (error.status === 401 && localStorage.getItem("refresh")) {
    $.ajax({
      url: "http://localhost:8000/api/token/refresh/",
      type: "POST",
      data: JSON.stringify({
        refresh: localStorage.getItem("refresh"),
      }),
      contentType: "application/json",
      success: function (response) {
        // Store the new access token
        localStorage.setItem("access", response.access);
        // return a flag to indicate that the request should be made again
        // due to the access token being refreshed
        canRequestAgain = true;
      },
      error: function (error) {
        // If couldn't refresh the access token, redirect to the login page
        console.log("before redirect");
        window.location.href = "login.html";
        console.log("after redirect");
        toastr.info("Your session has expired. Please log in again.", "Error");
      },
    });
  }
  if (canRequestAgain) {
    return true;
  }
  let message;
  if (error?.responseJSON?.detail) {
    message = error.responseJSON.detail;
  } else {
    message = optionalMessage || "An error occurred";
  }
  toastr.error(message, "Error");
}

function booleanToIconRenderer(data, type, row) {
  console.log(data);
  return data
    ? '<i class="fa-solid fa-circle-check" style="color: #31c97a;"></i>'
    : '<i class="fa-solid fa-circle-xmark" style="color: #e23232;"></i>';
}
