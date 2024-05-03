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

  function toggleSections(section1Id, section2Id) {
    var section1 = document.getElementById(section1Id);
    var section2 = document.getElementById(section2Id);

    if (section1.classList.contains("hidden_sect")) {
        section1.classList.remove("hidden_sect");
        section2.classList.add("hidden_sect");
    } else {
        section1.classList.add("hidden_sect");
        section2.classList.remove("hidden_sect");
    }
}