$(document).ready(function(){
  // When the document is ready, make two global elements containing the selects
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
