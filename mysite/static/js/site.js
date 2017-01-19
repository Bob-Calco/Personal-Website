function pageload(){
    // color the active tab
    title = document.title
    if (title == "Home | Bob"){
        document.getElementById('home-link').className += " home-active"
    }
    else if (title == "About | Bob"){
        document.getElementById('about-link').className += " about-active"
    }
    else if (title == "Projects | Bob"){
        document.getElementById('projects-link').className += " projects-active"
    }
}

// PAGE: Projects
// does all the stuff to toggle the drop down thingies
function projectDropDownToggle(id, icon){
  if (document.getElementById(id).className == "projects-dd") {
    document.getElementById(id).className += " active";
    document.getElementById(id).style.opacity = 1;
    document.getElementById(id).style.maxHeight = '500px';
    icon.style.WebkitTransform = "rotate(180deg)";

  }
  else {
    document.getElementById(id).className = "projects-dd";
    document.getElementById(id).style.maxHeight = '0px';
    document.getElementById(id).style.opacity = 0;
    icon.style.WebkitTransform = "rotate(0deg)";
  }
}

// PAGE: About
// functions for the carousel
var slideNumber = 0;
function showSlide(delta){
    slides = document.getElementsByClassName('slide');
    slideNumber += delta;
    if(slideNumber >= slides.length){
        slideNumber = 0;
    }
    if(slideNumber < 0){
        slideNumber = slides.length -1;
    }
    for(i = 0; i < slides.length; i++){
        slides[i].className = 'slide hidden';
        if(i === slideNumber){
            slides[i].className = 'slide';
        }
    }
}
