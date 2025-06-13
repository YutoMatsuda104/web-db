document.querySelector("form").addEventListener("submit", function(event) {
  let submitButton = this.querySelector("[type=submit]");
  submitButton.disabled = true;
  
  setTimeout(function() {
    submitButton.disabled = false;
  }, 10000);
});

document.getElementById("cancel").addEventListener("click", function() {
  history.back();
});
