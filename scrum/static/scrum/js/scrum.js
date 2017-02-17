function pbtabToggle(tab){
  var a = document.getElementsByClassName("tab");
  for (var i = 0; i<a.length; i++){
    a[i].className = "tab hidden";
  }
  document.getElementById('tab1Link').className = "";
  document.getElementById('tab2Link').className = "";
  document.getElementById(tab+'Link').className = "active-tab";
  document.getElementById(tab).className = "tab";
}
