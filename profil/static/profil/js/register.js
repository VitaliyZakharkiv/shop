function showPasswords(){
    let parol = document.getElementById('id_password1');
    let parol_again = document.getElementById('id_password2');
    let icon = document.getElementById("password_icon");
    if (parol.type === "password"){
    	if (parol_again.type === "password"){
    	    parol.type = "text";
    	    parol_again.type = "text";
    	    icon.style.backgroundImage = 'url("/static/profil/img/eye (3).png")';
    	}
    }
    else{
        parol.type = "password";
        parol_again.type = "password";
        icon.style.backgroundImage = 'url("/static/profil/img/eye (4).png")';
    }
}