$(document).ready(function(){
  var url = $('#wait-message').data('url');
  document.getElementById('wait-message').innerHTML = "Processing data, please wait";
  $.ajax({
    url : url,
    type : "GET",
    success : function(data){
      window.location.replace(data.url);
    },
    error: function(xhr,errmsg,err){
      console.log(xhr.status + ": " + xhr.responseText);
    },
  })
});
