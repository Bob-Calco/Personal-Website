/* Navigation thingie */
function dropdown(){
  if (document.getElementById("dropdown-menu").style.display === "none"){
    document.getElementById("dropdown-menu").style.display = "inline-block";

    document.getElementById('body').addEventListener('click', dropdownHide);
  }
  else {
    document.getElementById("dropdown-menu").style.display = "none";
  }
}

/* listener to close the dropdown menu */
function dropdownHide(e){
  if(e.target != document.getElementById("dropdown-menu") && e.target != document.getElementById('dropdown-button')){
    document.getElementById("dropdown-menu").style.display = "none";
    document.getElementById("body").removeEventListener('click', dropdownHide);
  }
}
