function pageLoad(){
  cryptChange();
  cipherChange();
}

function hello(){
  event.preventDefault();
  $.ajax({
    url : "encryption/",
    type : "POST",
    data : $("#form").serialize(),

    success : function(data){
      document.getElementById('response').innerHTML = data;
      console.log("check")},
    error : function(xhr,errmsg,err){
      console.log(xhr.status + ": " + xhr.responseText);
    }
  })
};



function cryptChange(){
  if(document.getElementById('id_crypt').value == "encrypt"){
    document.getElementById('decrypt-keys').className = 'hidden';
  }
  else if (document.getElementById('id_crypt').value == "decrypt"){
    if (!(document.getElementById('id_method').value == "atbash")){
      document.getElementById('decrypt-keys').className = '';
    }

    document.getElementById('id_int_key1').required = false;
    document.getElementById('id_int_key2').required = false;
  }
}

function cipherChange(){
  if(document.getElementById('id_method').value == 'caesar'){

    document.getElementById('key1').className = '';
    document.getElementById('key2').className = 'hidden';

    if(document.getElementById('id_crypt') == 'encrypt'){
      document.getElementById('id_int_key1').required = true;
      document.getElementById('id_int_key2').required = false;
    }

    document.getElementById('caesar').className = '';
    document.getElementById('affine').className = 'hidden';
    document.getElementById('atbash').className = 'hidden';
  }
  else if(document.getElementById('id_method').value == 'affine'){

    document.getElementById('key1').className = '';
    document.getElementById('key2').className = '';

    if(document.getElementById('id_crypt') == 'encrypt'){
      document.getElementById('id_int_key1').required = true;
      document.getElementById('id_int_key2').required = true;
    }


    document.getElementById('caesar').className = 'hidden';
    document.getElementById('affine').className = '';
    document.getElementById('atbash').className = 'hidden';
  }
  else if(document.getElementById('id_method').value == 'atbash'){

    document.getElementById('key1').className = 'hidden';
    document.getElementById('key2').className = 'hidden';

    if(document.getElementById('id_crypt') == 'encrypt'){
      document.getElementById('id_int_key1').required = false;
      document.getElementById('id_int_key2').required = false;
    }

    document.getElementById('decrypt-keys').className = 'hidden';
    document.getElementById('caesar').className = 'hidden';
    document.getElementById('affine').className = 'hidden';
    document.getElementById('atbash').className = '';
  }
}
