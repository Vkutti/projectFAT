window.onload = function() {
  const loadingScreen = document.querySelector(".loading-screen");
  const content = document.querySelector(".content");

  setTimeout(() => {
      loadingScreen.style.display = "none";
      content.style.display = "block";
  }, 750);
};