


function hideElement(elem_id){
    var elem = document.getElementById(elem_id);
    elem.style.opacity = 0;
    // elem.style.visibility = "hidden";
}

function showElement(elem_id){
    var elem = document.getElementById(elem_id);
    elem.style.opacity = 1;
    // elem.style.visibility = "visible";
}


function elementTransitionIn(elem_id){
    window.setTimeout(function() {
        showElement(elem_id);
    }, 100);
}

function elementTransitionOut(elem_id){
    window.setTimeout(function() {
        hideElement(elem_id);
    }, 100);
}
