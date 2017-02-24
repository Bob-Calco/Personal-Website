/* Toggle the tabs on the Product Backlog */
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

/* Submit userstory */
function submitUserstory(){
  event.preventDefault();
  $.ajax({
    url : "add-userstory/",
    type : "POST",
    data : $("#userstoryForm").serialize(),

    success : function(data){
      return;
    },
    error : function(xhr,errmsg,err){
      console.log(xhr.status + ": " + xhr.responseText);
    }
  })
  document.getElementById('id_us-name').value = "";
  document.getElementById('id_us-goal').value = "";
  document.getElementById('id_us-epic').value = "";
};

/* submit epic */
function submitEpic(){
  event.preventDefault();
  $.ajax({
    url : "add-epic/",
    type : "POST",
    data : $("#epicForm").serialize(),

    success : function(data){
      return;
    },
    error : function(xhr,errmsg,err){
      console.log(xhr.status + ": " + xhr.responseText);
    }
  })
  document.getElementById('id_epic-name').value = "";
  document.getElementById('id_epic-goal').value = "";
};
