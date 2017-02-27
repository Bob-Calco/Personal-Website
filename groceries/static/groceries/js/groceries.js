/* Navigation thingie */
function dropdown(){
  if (document.getElementById("dropdown-menu").style.display === "none"){
    document.getElementById("dropdown-menu").style.display = "inline-block";
  }
  else {
    document.getElementById("dropdown-menu").style.display = "none";
  }
}

/* show import form for recipes */
function toggleImportForm(){
  if(document.getElementById("importForm").className = "import-form hidden"){
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
