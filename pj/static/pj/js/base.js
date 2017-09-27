function toggleMenu(){
  var nav = document.getElementById('nav-links');
  var content = document.getElementById('content');
  if (nav.classList.contains('nav-active')){
    nav.classList.remove('nav-active');
    content.classList.remove('hidden');
  }
  else {
    nav.classList.add('nav-active');
    content.classList.add('hidden');
  }
}
