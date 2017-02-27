/* Mark recipe items for deletion */
function recipeItemDelete(){
  items = document.getElementsByClassName("deletionMarker");
  for (var i = 0; i < items.length; i++){
    if (items[i].childNodes[1].firstChild.value.trim() === ""){
      items[i].childNodes[5].firstChild.checked = true;
    }
  }
}

/* add new form and remove/set oninput attribute */
function addForm(form){
  var clone = document.getElementById("empty_"+form+"form").cloneNode(true);
  var formid = document.getElementById("id_"+form+"-TOTAL_FORMS").value;

  clone.innerHTML = clone.innerHTML.replace(new RegExp("__prefix__", 'g'), formid);
  clone.removeAttribute('id');
  clone.className = "deletionMarker";
  document.getElementById(form+"Form").children[4].children[0].appendChild(clone);
  document.getElementById("id_"+form+"-TOTAL_FORMS").value = Number(formid) + 1;

  document.getElementById('id_item-'+ formid +'-description').setAttribute("oninput", "addForm('item')");
  document.getElementById('id_item-' + (formid-1) + '-description').setAttribute("oninput", "");
}

/* add initial oninput */
window.onload = function pageLoad(){
  var formid = document.getElementById("id_item-TOTAL_FORMS").value - 1;
  document.getElementById('id_item-'+ formid +'-description').setAttribute("oninput", "addForm('item')");
  console.log('check')
}
