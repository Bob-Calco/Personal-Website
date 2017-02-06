function dropdown(){
  if (document.getElementById("dropdown-menu").style.display === "none"){
    document.getElementById("dropdown-menu").style.display = "inline-block";
  }
  else {
    document.getElementById("dropdown-menu").style.display = "none";
  }
}

function addForm(form){
  var clone = document.getElementById("empty_"+form+"form").cloneNode(true);
  var formid = document.getElementById("id_"+form+"-TOTAL_FORMS").value;

  clone.innerHTML = clone.innerHTML.replace(new RegExp("__prefix__", 'g'), formid);
  clone.removeAttribute('id');
  clone.className = "";
  document.getElementById(form+"Form").children[5].children[0].appendChild(clone);

  document.getElementById("id_"+form+"-TOTAL_FORMS").value = Number(formid) + 1;
}
