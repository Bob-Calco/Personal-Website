function toggleMenu(){
  var nav = document.getElementById('nav-links')
  if (nav.classList.contains('nav-active')){
    nav.classList.remove('nav-active');
  }
  else {
    nav.classList.add('nav-active');
  }
}
