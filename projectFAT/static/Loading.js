// Optimize loading screen functionality
document.addEventListener('DOMContentLoaded', function() {
  const loadingScreen = document.querySelector(".loading-screen");
  const content = document.querySelector(".content");
  
  // Preload any critical resources here
  
  // Show content when page is ready
  setTimeout(() => {
      loadingScreen.style.display = "none";
      content.style.display = "block";
      document.body.classList.add('loaded');
  }, 750);
});