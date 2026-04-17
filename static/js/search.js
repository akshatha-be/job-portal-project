// Auto-dismiss alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (alert) {
      var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    });
  }, 4000);

  // Navbar scroll effect
  var nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 50) {
        nav.style.boxShadow = '0 4px 30px rgba(0,0,0,0.4)';
      } else {
        nav.style.boxShadow = '0 2px 20px rgba(0,0,0,0.25)';
      }
    });
  }
});
