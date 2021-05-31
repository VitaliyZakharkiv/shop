// Show password
function showPassword(){
    let parol = document.getElementById('id_password');
    let icon = document.getElementById("password_icon");
    if (parol.type === "password"){
        parol.type = "text";
        icon.style.backgroundImage = 'url("/static/profil/img/eye (3).png")';
    }
    else{
        parol.type = "password";
        icon.style.backgroundImage = 'url("/static/profil/img/eye (4).png")';
    }
}

// Error message
var close = document.getElementsByClassName("closebtn");
var i;

for (i = 0; i < close.length; i++) {
  close[i].onclick = function(){

    var div = this.parentElement;

    div.style.opacity = "0";

    setTimeout(function(){ div.style.display = "none"; }, 600);
  };
}