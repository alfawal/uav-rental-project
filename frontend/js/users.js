$(document).ready(function () {
  let accessToken = getAccessToken();
  let tokenIsUpdated = false;
  
  const usersTable = $("#usersTable").DataTable({
    processing: true,
    serverSide: true,
    ajax: {
      url: "http://localhost:8000/api/users/",
      type: "GET",
      headers: {
        Authorization: "Bearer " + accessToken,
      },
      data: dataTableQueryParamsHandler,
      dataFilter: function (data) {
        var json = jQuery.parseJSON(data);
        json.recordsTotal = json.total_count;
        json.recordsFiltered = json.count;
        json.data = json.results;
        return JSON.stringify(json);
      },
      error: function (error) {
        tokenIsUpdated = ajaxErrorHandler(
          error,
          "An error occurred while fetching users"
        );
      },
    },
    columns: [
      { data: "id" },
      { data: "username" },
      { data: "email" },
      { data: "is_active", render: booleanToIconRenderer },
      { data: "is_superuser", render: booleanToIconRenderer },
      { data: "is_staff", render: booleanToIconRenderer },
      { data: "is_customer", render: booleanToIconRenderer },
    ],
  });

  // Refresh the users table every 5 minutes
  const refreshIntervalMilliseconds = 5 * 60 * 1000;
  setInterval(function () {
    usersTable.ajax.reload(null, false);
    if (tokenIsUpdated) {
      accessToken = getAccessToken();
      usersTable.ajax.reload(null, false);
      tokenIsUpdated = false;

    }
  }, refreshIntervalMilliseconds);
});
