$(document).ready(function(){

  $('td:first-child').click(function(){get_form(this)});

  /*$('#add-transaction').click(function(){
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
  })*/
});

function get_form(tr){
  if (document.getElementById("popup-form").classList.contains('hidden')){
    var url = $(tr).data("url");
    $.ajax({
      url : url,
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
  setup_post(form)
  $('#form-close').click(function(){
    var form = document.getElementById('popup-form');
    form.classList.add('hidden');
    form.innerHTML = "";
  })
}

function setup_post(form){
  $('#save-button').click(function(){
    var id = $('#category-form').data('id');
    var url = $('#category-form').data('url');
    event.preventDefault();
    $.ajax({
      url : url,
      type : "POST",
      data : $('#category-form').serialize(),
      success : function(data){
        $('#category-form').remove();
        var form = document.getElementById('popup-form');
        if (data.saved){
          var tr = document.createElement('tr');
          tr.innerHTML = data.html;
          tr.firstElementChild.onclick = function(){get_form(tr.firstElementChild)};
          form.classList.add('hidden');
          if (data.add){
            if (data.specification_of) {
              var td_parent = document.querySelector("td[data-id='" + data.specification_of + "']").nextElementSibling;
              var last_row = td_parent.firstElementChild.firstElementChild.lastElementChild;
              last_row.insertAdjacentElement('beforebegin', tr)
            }
            else {
              if (data.is_income == '1') {
                var table = document.getElementById('income-table');
              }
              else {
                var table = document.getElementById('expense-table');
              }
              var last_row = table.children[1].lastElementChild;
              var td = tr.lastElementChild.firstElementChild.firstElementChild.firstElementChild.firstElementChild;
              td.onclick = function(){get_form(td)};
              last_row.insertAdjacentElement('beforebegin', tr)
            }
          }
          else {
            var td = document.querySelector("td[data-id='" + id + "']");
            td.innerHTML = data.html;
          }
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
