function processTransaction(){
  /* make new div in the middle of the screen with an add transaction form
  the table row will be at the top for reference
  the rest of the webpage gets a darker color */
  var form = document.getElementById("add_transaction")
  if (form.classList.contains("hidden")){
    form.classList.remove("hidden")
  }
}

function closeForm(){
  var form = document.getElementById("add_transaction")
  form.classList.add("hidden")
}

function submitTransaction(){
  event.preventDefault();
  $.ajax({
    url : "process/",
    type : "POST",
    data : $("#transaction-form").serialize(),
    success : function(data){
      if (data.saved){
        var form = document.getElementById("add_transaction")
        form.classList.add("hidden")
      }
      else {
        var form = document.getElementById("add_transaction")
        form.classList.add("hidden")
      }
    },
    error: function(xhr,errmsg,err){
      console.log(xhr.status + ": " + xhr.responseText);
    },
  })
}

function hideColumn(){
  /* hide column, later also store this as a setting for this dataset */
}

function deleteItem(id){
  $.ajax({
    url : "delete/" + id + "/",
    type : "POST",
    beforeSend: function(xhr, settings){
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function(data){
      if (data.deleted){
        document.getElementById(id).remove();
      }
    },
    error: function(xhr,errmsg,err){
      console.log(xhr.status + ": " + xhr.responseText);
    }
  })
};

$(document).ready(function(){
  document.getElementById('id_category').onchange = change_specifications;
  var options = document.getElementById('id_category').children;
  for(var i = options.length-1; i > 0; i--){
    if(!(options[i].textContent in category_data)){
      document.getElementById('id_category').removeChild(options[i]);
    }
  }
  specifications_template = document.getElementById('id_specification').cloneNode(true);
  change_specifications()
});

function change_specifications(){
  var parent = document.getElementById('id_specification').parentNode;
  parent.removeChild(document.getElementById('id_specification'));
  var template = specifications_template.cloneNode(true);
  var category = document.getElementById('id_category').options[document.getElementById('id_category').selectedIndex].text;

  if(/^--+/.test(category)){
    var options = template.children;
    for(var i = options.length-1; i > 0; i--){
      template.removeChild(options[i]);
    }
    parent.appendChild(template);
  }
  else {
    var specifications = category_data[category];
    var options = template.children;
    for(var i = options.length-1; i > 0; i--){
      if(specifications.indexOf(options[i].textContent) == -1){
        template.removeChild(options[i]);
      }
    }
    parent.appendChild(template);
  }
}
