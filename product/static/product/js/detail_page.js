//Показ блоків фільтрів
let show = true;

function showFilter(a, b) {
  if (show){
    document.getElementById(a).style.display = "none";
    document.getElementById(b).style.transform = "rotate(0deg)";
    document.getElementById(b).style.transition = "transform .3s ease";
    show = false;
  }else {
    document.getElementById(a).style.display = "block";
    document.getElementById(b).style.transform = "rotate(90deg)";
    document.getElementById(b).style.transition = "transform .3s ease";
    show = true;
  }
}
