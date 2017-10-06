$(document).ready(function(){
  var year_tabs = document.getElementById('years').children;
  for (var i = 0; i < year_tabs.length; i++){
    if (year_tabs[i].firstChild.innerText == year){
      year_tabs[i].firstChild.classList.add('active');
      break;
    }
  }
  var month_tabs = document.getElementById('months').children;
  month_tabs[parseInt(month)-1].firstChild.classList.add('active');
  $('.transactions').click(function(){get_form_from_instance(this)});
  $('#add-transaction').click(function(){
    if (document.getElementById("popup-form").classList.contains('hidden')){
      $.ajax({
        url : "/finances/transaction/add/",
        type : "GET",
        success : function(data){
          var form = document.getElementById('popup-form')
          form.innerHTML = data.html;
          form.classList.remove("hidden");
          setup_form(form);
        },
        error: function(xhr,errmsg,err){
          console.log(xhr.status + ": " + xhr.responseText);
        },
      })
    }
  })
});

function get_form_from_instance(tr){
  if (document.getElementById("popup-form").classList.contains('hidden')){
    var id = $(tr).data("id");
    $.ajax({
      url : "/finances/transaction/" + id + "/",
      type : "GET",
      success : function(data){
        var form = document.getElementById('popup-form')
        form.innerHTML = data.html;
        form.classList.remove("hidden");
        setup_form(form);
      },
      error: function(xhr,errmsg,err){
        console.log(xhr.status + ": " + xhr.responseText);
      },
    })
  }
}

function setup_form(form){
  setup_categories()
  setup_post(form)
  $('#form-close').click(function(){
    var form = document.getElementById('popup-form');
    form.classList.add('hidden');
    form.innerHTML = "";
  })
}

function setup_post(form){
  $('#save-button').click(function(){
    var add = $('#transaction-form').data('add');
    if (add == 'False'){
      var id = $('#transaction-form').data("instance-id");
      var url = "/finances/transaction/" + id + "/";
    }
    else {
      var url = "/finances/transaction/add/";
    }
    event.preventDefault();
    $.ajax({
      url : url,
      type : "POST",
      data : $('#transaction-form').serialize(),
      success : function(data){
        $('#transaction-form').remove();
        var form = document.getElementById('popup-form');
        if (data.saved){
          form.classList.add('hidden');
          form.innerHTML = "";
          if (data.add){
            var tr = document.getElementById('transaction-table-body').appendChild(document.createElement('tr'));
            tr.classList.add('transactions')
            tr.setAttribute('data-id', data.t_id)
            tr.onclick = function(){get_form_from_instance(tr)};
          }
          else {
            var tr = document.querySelector("tr[data-id='" + id + "']");
          }
          tr.innerHTML = data.html;
        }
        else {
          form.innerHTML = data.html;
        }
      },
      error: function(xhr,errmsg,err){
        console.log(xhr.status + ": " + xhr.responseText);
      },
    })
  });
}

function setup_categories() {
  document.getElementById('id_category').onchange = change_specifications;
  var options = document.getElementById('id_category').children;
  for(var i = options.length-1; i > 0; i--){
    if(!(options[i].textContent in category_data)){
      document.getElementById('id_category').removeChild(options[i]);
    }
  }
  specifications_template = document.getElementById('id_specification').cloneNode(true);
  change_specifications()
}

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
