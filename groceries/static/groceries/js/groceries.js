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

/* show import form for recipes */
function toggleImportForm(){
  if(document.getElementById("importForm").className == "import-form hidden"){
    document.getElementById("importForm").className = "import-form";
  }
  else{
    document.getElementById("importForm").className = "import-form hidden";0
  }
}

/* Grocery list checkmarks */
function check(item){
  document.getElementById(item).style.display = "None";
}
