/* submit extra item and add to list */
function sendMessage(){
  event.preventDefault();
  $.ajax({
    url : "",
    type : "POST",
    data : $("#message").serialize(),

    success : function(data){
      json = data[0];
      var li = document.createElement('li');
      if(json['fields']['reply'] == true){
        li.className = "message reply";
      }
      else {
        li.className = "message";
      }
      var p1 = document.createElement('p');
      p1.className = "content";
      p1.innerHTML = json['fields']['content'];
      var p2 = document.createElement('p');
      p2.className = "date";
      p2.innerHTML = "just now";

      li.appendChild(p1);
      li.appendChild(p2);
      document.getElementById('messages').appendChild(li);
    },
    error : function(xhr,errmsg,err){
      console.log(xhr.status + ": " + xhr.responseText);
    }
  })
  document.getElementById('id_content').value = "";
};

/* check for new messages */
function checkMessages(){
  $.ajax({
    url : "check-messages/",
    type : "GET",

    success : function(data){
      for(json in data){
        json = data[0];
        var li = document.createElement('li');
        if(json['fields']['reply'] == true){
          li.className = "message reply";
        }
        else {
          li.className = "message";
        }
        var p1 = document.createElement('p');
        p1.className = "content";
        p1.innerHTML = json['fields']['content'];
        var p2 = document.createElement('p');
        p2.className = "date";
        p2.innerHTML = "just now";

        li.appendChild(p1);
        li.appendChild(p2);
        document.getElementById('messages').appendChild(li);
      }
    },
    error : function(xhr,errmsg,err){
      console.log(xhr.status + ": " + xhr.responseText);
    }
  })
};

/* start checking for new messages every 5 seconds */
var check = setInterval(checkMessages, 5000);
