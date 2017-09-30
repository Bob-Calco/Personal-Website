function toggleMenu(){
  var nav = document.getElementById('nav-links');
  var content = document.getElementById('content');
  var mobileButton = document.getElementById('mobileMenu');
  if (nav.classList.contains('nav-active')){
    nav.classList.remove('nav-active');
    content.classList.remove('hidden');
    mobileButton.innerHTML = "&#9776";
  }
  else {
    nav.classList.add('nav-active');
    content.classList.add('hidden');
    mobileButton.innerHTML = "X";
  }
}
