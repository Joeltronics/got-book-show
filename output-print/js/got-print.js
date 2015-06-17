var spoilerclasses = "spoiler_notonshow";
var colorclasses = "cpov";
var booksExpanded = [true,true,true,true,true,true];

function expandbook(n) {
	var divs = document.getElementsByClassName("b" + n);
	for(var i = 0; i < divs.length; i++) { divs[i].style.display="table-cell"; }
	
	divs = document.getElementsByClassName("b" + n + "c");
	for(var i = 0; i < divs.length; i++) { divs[i].style.display="none"; }

	if (n != 45) {
		booksExpanded[n-1] = true;
	} else {
		booksExpanded[3] = true;
		booksExpanded[4] = true;
	}
}

function collapsebook(n) {
	var divs = document.getElementsByClassName("b" + n);
	for(var i = 0; i < divs.length; i++) { divs[i].style.display="none"; }
	
	divs = document.getElementsByClassName("b" + n + "c");
	for(var i = 0; i < divs.length; i++) { divs[i].style.display="table-cell"; }

	if (n != 45) {
		booksExpanded[n-1] = false;
	} else {
		booksExpanded[3] = false;
		booksExpanded[4] = false;
	}	
}

function getClassAsArray(className) {
	return Array.prototype.slice.call(document.getElementsByClassName(className));
}

function combine45() {

	var divsShow = [];
	var divsHide = [];

	var combine = (getQueryVariable("combine") != false)

	if(combine) {
		if(booksExpanded[3] || booksExpanded[4]) {
			divsShow = divsShow.concat(getClassAsArray("b45"));
			divsHide = divsHide.concat(getClassAsArray("b45c"));
		} else {
			divsShow = divsShow.concat(getClassAsArray("b45c"));
			divsHide = divsHide.concat(getClassAsArray("b45"));
		}

		divsHide = divsHide.concat(getClassAsArray("b4"));
		divsHide = divsHide.concat(getClassAsArray("b5"));
		divsHide = divsHide.concat(getClassAsArray("b4c"));
		divsHide = divsHide.concat(getClassAsArray("b5c"));

	} else {

		if(booksExpanded[3]) {
			divsShow = divsShow.concat(getClassAsArray("b4"));
			divsHide = divsHide.concat(getClassAsArray("b4c"));
		} else {
			divsShow = divsShow.concat(getClassAsArray("b4c"));
			divsHide = divsHide.concat(getClassAsArray("b4"));
		}
		
		if(booksExpanded[4]) {
			divsShow = divsShow.concat(getClassAsArray("b5"));
			divsHide = divsHide.concat(getClassAsArray("b5c"));
		} else {
			divsShow = divsShow.concat(getClassAsArray("b5c"));
			divsHide = divsHide.concat(getClassAsArray("b5"));
		}

		divsHide = divsHide.concat(getClassAsArray("b45"));
		divsHide = divsHide.concat(getClassAsArray("b45c"));
	}

	for(var i = 0; i < divsShow.length; i++) { divsShow[i].style.display="table-cell"; }
	for(var i = 0; i < divsHide.length; i++) { divsHide[i].style.display="none"; }

	var b45info = getClassAsArray("b45info");

	if(combine) {
		for(var i = 0; i < b45info.length; i++) { b45info[i].style.display="block"; }
	} else {
		for(var i = 0; i < b45info.length; i++) { b45info[i].style.display="none"; }
	}
}

function floatleft() {

	// FIXME this is probably broken

	var hideonfloatdivs = getClassAsArray("hideonfloat");

	if(getQueryVariable("float")) {
		
		// Hide 'hideonfloat'
		for(var i = 0; i < hideonfloatdivs.length; i++) { hideonfloatdivs[i].style.display="none"; }

		// Show 'floatingtable'
		document.getElementById("floatingtable").style.display="block";

		// Move maintable left 1 pixel so you don't get double-thickness border
		document.getElementById("maintable").style.left="-1px";

	} else {
		
		// Show 'hideonfloat'
		for(var i = 0; i < hideonfloatdivs.length; i++) { hideonfloatdivs[i].style.display="table-cell"; }

		// Hide 'floatingtable'
		document.getElementById("floatingtable").style.display="none";

		// Move maintable back to original position
		document.getElementById("maintable").style.left="0px";
	}
}

function resetdivs() {
	var div = document.getElementById("tablediv");
	div.className = colorclasses + " " + spoilerclasses;
}

function colorby() {

	var color = (getQueryVariable("color") != false)

	if (color) {
		colorclasses = "cpov";
	} else {
		colorclasses = "cnone";
	}

	resetdivs();
}

function setspoilers() {
	var n = parseInt(getQueryVariable("spoilers"));
	spoilerclasses = "";
	switch(n) {
		case 0: spoilerclasses += "spoiler_notonshow"; break;
		case 1: spoilerclasses += "spoiler_b6"; break;
		case 2: spoilerclasses += ""; break;
	}
	resetdivs();
}

/* Get query string */
function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if(pair[0] == variable){
			//alert(variable + "=" + pair[1]); // DEBUG
        	return pair[1];
        }
    }
    return(false);
}

function onload() {
	setspoilers();
	//floatleft(); // FIXME
	combine45();
	colorby();
	resetdivs();
}
