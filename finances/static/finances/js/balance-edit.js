/* Mark balances for deletion */
function presubmitCheck(){
  items = document.getElementsByClassName("marker");
  /* Check for items that need to be deleted */
  for (var i = 0; i < items.length; i++){
    if (items[i].childNodes[3].firstChild.value.trim() === ""){
      items[i].childNodes[7].firstChild.checked = true;
    }
  }
  /* add the date to all the items */
  for (var i = 0; i < items.length; i++){
    items[i].childNodes[9].firstChild.value = year+"-"+month+"-1";
  }
}

/* add new form and remove/set oninput attribute */
function addForm(){
  var clone = document.getElementById("empty_balanceform").cloneNode(true);
  var formid = document.getElementById("id_form-TOTAL_FORMS").value;

  clone.innerHTML = clone.innerHTML.replace(new RegExp("__prefix__", 'g'), formid);
  clone.removeAttribute('id');
  clone.className = "marker";
  document.getElementById("balance-form").children[5].children[1].appendChild(clone);
  document.getElementById("id_form-TOTAL_FORMS").value = Number(formid) + 1;

  document.getElementById('id_form-'+ formid +'-item').setAttribute("onchange", "addForm()");
  document.getElementById('id_form-' + (formid-1) + '-item').setAttribute("onchange", "");
}

/* add initial oninput */
window.onload = function pageLoad(){
  var formid = document.getElementById("id_form-TOTAL_FORMS").value - 1;
  document.getElementById('id_form-'+ formid +'-item').setAttribute("onchange", "addForm()");
}
