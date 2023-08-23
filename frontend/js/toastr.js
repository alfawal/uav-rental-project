// toastr notification configuration
toastr.options = {
  closeButton: true,
  debug: false,
  newestOnTop: true,
  progressBar: true,
  positionClass: "toast-top-center",
  preventDuplicates: true,
  onclick: function () {
    toastr.clear(); // Close the toastr notification when clicked
  },
  showDuration: "300",
  hideDuration: "1000",
  timeOut: "4000",
  extendedTimeOut: "1000",
//   showDuration: "100000000",
//   hideDuration: "100000000",
//   timeOut: "100000000",
//   extendedTimeOut: "100000000",
  showEasing: "swing",
  hideEasing: "linear",
  showMethod: "fadeIn",
  hideMethod: "fadeOut",
};

// Create a <style> element
const styleElement = document.createElement('style');

// Add CSS rules to the <style> element
styleElement.innerHTML = `
  #toast-container {
    margin-top: 20px;
  }

  #toast-container .toast {
    width: 450px !important;
  }
`;

// Append the <style> element to the <head> section of the document
document.head.appendChild(styleElement);
