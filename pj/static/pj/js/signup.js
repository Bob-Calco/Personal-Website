$(document).ready(function(){
  document.getElementById('id_role').onchange = roleSelected;
  document.getElementById('id_class_change').onchange = classChangeSelected;
  document.getElementById('last_class').classList.add('hidden');
  document.getElementById('class_change').classList.add('hidden');
  document.getElementById('class_change_year').classList.add('hidden');
})

function roleSelected(){
  var role = document.getElementById('id_role').options[document.getElementById('id_role').selectedIndex].text;
  if (role != 'Leerling'){
    document.getElementById('last_class').classList.add('hidden');
    document.getElementById('class_change').classList.add('hidden');
    document.getElementById('class_change_year').classList.add('hidden');
  }
  else {
    document.getElementById('last_class').classList.remove('hidden');
    document.getElementById('class_change').classList.remove('hidden');
    document.getElementById('id_class_change_year').selectedIndex = 0;
  }
}

function classChangeSelected(){
    var change = document.getElementById('id_class_change').options[document.getElementById('id_class_change').selectedIndex].text;

    if(change == 'Blijven zitten'){
      document.getElementById('class_change_year').classList.remove('hidden');
    }
    else if (change == 'Klas overgeslagen'){
      document.getElementById('class_change_year').classList.remove('hidden');
    }
    else {
      document.getElementById('class_change_year').classList.add('hidden');
      document.getElementById('id_class_change_year').selectedIndex = 0;
    }
}
