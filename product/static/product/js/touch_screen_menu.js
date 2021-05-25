
document.getElementById("bg").onclick = function () {
    open()
};

function open() {
    document.getElementById("nms").classList.toggle("active");
    document.getElementById("bg").classList.toggle("show");
    document.getElementById("body").classList.toggle("lock");
}

let visible = true;

function showCategory(a, b) {
  if (visible){
    document.getElementById(a).style.display = "none";
    document.getElementById(b).style.transform = "rotate(0deg)";
    document.getElementById(b).style.transition = "transform .3s ease";
    visible = false;
  }else {
    document.getElementById(a).style.display = "block";
    document.getElementById(b).style.transform = "rotate(90deg)";
    document.getElementById(b).style.transition = "transform .3s ease";
    visible = true;
  }
}