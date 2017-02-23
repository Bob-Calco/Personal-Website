/* Navigation thingie */
function dropdown(){
  if (document.getElementById("dropdown-menu").style.display === "none"){
    document.getElementById("dropdown-menu").style.display = "inline-block";
  }
  else {
    document.getElementById("dropdown-menu").style.display = "none";
  }
}

/* New and Edit recipe page */
function addForm(form){
  var clone = document.getElementById("empty_"+form+"form").cloneNode(true);
  var formid = document.getElementById("id_"+form+"-TOTAL_FORMS").value;

  clone.innerHTML = clone.innerHTML.replace(new RegExp("__prefix__", 'g'), formid);
  clone.removeAttribute('id');
  clone.className = "";
  document.getElementById(form+"Form").children[4].children[0].appendChild(clone);

  document.getElementById("id_"+form+"-TOTAL_FORMS").value = Number(formid) + 1;
}

/* Grocery list checkmarks */
function check(item){
  document.getElementById(item).style.display = "None";
}

/* Mark recipe items for deletion */
function recipeItemDelete(){
  items = document.getElementsByClassName("deletionMarker");
  for (var i = 0; i < items.length; i++){
    if (items[i].childNodes[1].firstChild.value.trim() === ""){
      items[i].childNodes[5].firstChild.checked = true;
    }
  }
}
