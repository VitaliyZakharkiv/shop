function func(arg, modal_window){
    let elem = document.getElementsByClassName(modal_window);
    console.log(elem);
    for(var i=0; i<elem.length; i++)elem[i].style.display = arg;
    let elems = document.getElementsByClassName("grey");
    for(var i=0; i<elems.length; i++)elems[i].style.display = arg;
    console.log(elems);
}
