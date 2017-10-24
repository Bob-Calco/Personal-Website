$(document).ready(function(){
  $('td:first-child').click(function(){get_form(this)});
});

function get_form(td){
  if (document.getElementById("popup-form").classList.contains('hidden')){
    var url = $(td).data("url");
    $.ajax({
      url : url,
      type : "GET",
      success : function(data){
        var form = document.getElementById('popup-form')
        $('#popup-form').html(data.html);
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
  // add initial onchange thingy
  var formid = document.getElementById("id_form-TOTAL_FORMS").value - 1;
  document.getElementById('id_form-'+ formid +'-item').setAttribute("onchange", "addForm()");
}

function setup_post(form){
  $('#save-button').click(function(){
    var url = $('#balance-form').data('url');
    presubmitCheck()
    event.preventDefault();
    $.ajax({
      url : url,
      type : "POST",
      data : $('#balance-form').serialize(),
      success : function(data){
        $('#balance-form').remove();
        var form = document.getElementById('popup-form');
        if (data.saved){
          location.reload(true);
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
  var parent = document.getElementById("balance-form").children[5].children[1];
  parent.insertBefore(clone, parent.lastChild);
  document.getElementById("id_form-TOTAL_FORMS").value = Number(formid) + 1;
  document.getElementById('id_form-'+ formid +'-item').setAttribute("onchange", "addForm()");
  document.getElementById('id_form-' + (formid-1) + '-item').setAttribute("onchange", "");
}
