//TABS
const tabsBtn = document.querySelectorAll(".tabs__nav-btn");
const tabsItems = document.querySelectorAll(".tabs__item");

tabsBtn.forEach(onTabClick);

function onTabClick(item) {
    item.addEventListener("click", function() {
        let currentBtn = item;
        let tabId = currentBtn.getAttribute("data-tab");
        let currentTab = document.querySelector(tabId);

        if( ! currentBtn.classList.contains('active') ) {
            tabsBtn.forEach(function(item) {
                item.classList.remove('active');
            });

            tabsItems.forEach(function(item) {
                item.classList.remove('active');
            });

            currentBtn.classList.add('active');
            currentTab.classList.add('active');
        }
    });
}

document.querySelector('.tabs__nav-btn').click();


// SLIDER
var slideIndex = 1;
showSlide(slideIndex);

function plus1(n){
    showSlide(slideIndex += n);
}

function showSlide(n){
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


//ADD REVIEW
function addReview(arg){
    let elem = document.getElementsByClassName("add-review-form");
    for(var i=0; i<elem.length; i++)elem[i].style.display = arg;
    let elems = document.getElementsByClassName("grey");
    for(var i=0; i<elems.length; i++)elems[i].style.display = arg;
}

