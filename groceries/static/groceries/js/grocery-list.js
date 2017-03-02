/* show import form for recipes */
function toggleExtraForm(){
  if(document.getElementById("extraItemForm").className = "extra-item-form hidden"){
    document.getElementById("extraItemForm").className = "extra-item-form";
  }
}

function closePopup(){
  document.getElementById('extraItemForm').className = "extra-item-form hidden";
}

/* submit extra item and add to list */
function submitExtraItem(){
  event.preventDefault();
  $.ajax({
    url : "make/add-item/",
    type : "POST",
    data : $("#extraItemForm").serialize(),

    success : function(data){
      json = data[0];
      var li = document.createElement('li');
      li.setAttribute('id', json['pk']);
      var box = document.createElement('span');
      box.className = "gl-checkbox";
      box.setAttribute('onclick', "check("+json['pk']+")");
      var name = document.createElement('span');
      name.className = "gl-item";
      name.innerHTML = json['fields']['description'];
      li.appendChild(box);
      li.appendChild(name);

      document.getElementById('list').appendChild(li);
      console.log("check")},
    error : function(xhr,errmsg,err){
      console.log(xhr.status + ": " + xhr.responseText);
    }
  })
  document.getElementById('id_description').value = "";
};
