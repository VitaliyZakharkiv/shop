// SLIDER
var slideIndex = 1;
showSlides(slideIndex);
// setInterval(AutoSlider, 5000, 1);

// function AutoSlider(n){
// 	showSlides(slideIndex += n);
// }

function plus(n){
	showSlides(slideIndex += n);
}

function showSlides(n){
	var i;
	var slides = document.getElementsByClassName("slide");

	if(n > slides.length){
		slideIndex = 1;
	}else if(n < 1){
		slideIndex = slides.length;
	}
	for(i=0; i < slides.length; i++){
		slides[i].style.display = "none";
	}
	slides[slideIndex-1].style.display = "block";
}


// document.getElementById("bg").onclick = function () {
//     open()
// };
//
// function open() {
//     document.getElementById("nms").classList.toggle("active");
//     document.getElementById("bg").classList.toggle("show");
//     document.getElementById("body").classList.toggle("lock");
// }
//
// let visible = true;
//
// function showCategory(a, b) {
//   if (visible){
//     document.getElementById(a).style.display = "none";
//     document.getElementById(b).style.transform = "rotate(0deg)";
//     document.getElementById(b).style.transition = "transform .3s ease";
//     visible = false;
//   }else {
//     document.getElementById(a).style.display = "block";
//     document.getElementById(b).style.transform = "rotate(90deg)";
//     document.getElementById(b).style.transition = "transform .3s ease";
//     visible = true;
//   }
// }