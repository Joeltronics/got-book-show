/*
Game of Thrones chapters vs episodes chart
Copyright (c) 2013-2015, Joel Geddert

Software License:
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

/*
I am not a JavaScript programmer. This is probably not very good JavaScript.
And yes, I'm aware I probably could have just used jquery for most of this.
*/

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

	if(document.getElementsByName("combine45checkbox")[0].checked) {
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
}

function floatleft() {

	var hideonfloatdivs = getClassAsArray("hideonfloat");

	if(document.getElementsByName("floatleftcheckbox")[0].checked) {
		
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
	var sel = document.getElementsByName("colorselect")[0]
	var n = parseInt(sel.value);
	switch(n) {
		case 1: colorclasses = "csto"; break;
		case 2: colorclasses = "cpov"; break;
		case 3: colorclasses = "cloc"; break;
		default: colorclasses = "cnone";
	}
	resetdivs();
}

function colorbox() {
	if (document.getElementsByName("colorcheckbox")[0].checked) {
		colorclasses = "cpov";
	} else {
		colorclasses = "cnone";
	}

	resetdivs();
}

function setspoilers() {
	var sel = document.getElementsByName("spoilerselect")[0]
	var n = parseInt(sel.value);
	spoilerclasses = "";
	switch(n) {
		case 0: spoilerclasses += "spoiler_notonshow"; break;
		case 1: spoilerclasses += "spoiler_b6"; break;
		case 2: spoilerclasses += ""; break;
	}
	resetdivs();
}

function onload() {
	setspoilers();
	floatleft();
	combine45();
	colorby();
}
