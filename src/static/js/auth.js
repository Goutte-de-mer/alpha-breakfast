const passwordInput = document.querySelector('input[name="password"]');
const togglePassword = document.querySelector(".show-password");

togglePassword.addEventListener("click", () => {
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    togglePassword.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
  } else {
    passwordInput.type = "password";
    togglePassword.innerHTML = '<i class="fa-solid fa-eye"></i>';
  }
});
