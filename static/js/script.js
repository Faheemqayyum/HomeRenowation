function toggleOffCanvas() {
    document.getElementById('offcanvas').classList.toggle('active');
  }

  document.addEventListener('DOMContentLoaded', function() {
    const sidebarLinks = document.querySelectorAll('.sidebar ul li a');
    const currentURL = window.location.href;

    sidebarLinks.forEach(link => {
        if (link.href === currentURL) {
            link.classList.add('active');
        }
    });
});

  document.addEventListener('DOMContentLoaded', function() {
    var accBtn = document.querySelector('.accordion-btn');
    var accContent = document.querySelector('.accordion-content');
  
    // Toggle accordion content when button is clicked
    accBtn.addEventListener('click', function() {
      accContent.classList.toggle('active');
      if (accContent.style.display === "flex") {
        accContent.style.display = "none";
      } else {
        accContent.style.display = "flex";
      }
    });
  });
  