var search = document.getElementById("search")
var header = document.getElementById("header")
var nav = document.getElementById("nav")
var search_input = document.getElementById("search_input")

function show_search() {
    search.style.visibility = "visible"
    search.style.transform = "translateY(0)"
    search.style.zIndex = 0
    nav.style.boxShadow = "none"
    setTimeout(()=> {search_input.focus()}, 700)
}

function hide_search() {
    search.style.transform = "translateY(-70px)"
    search.style.zIndex = -1;
    search.style.visibility = "hidden"

    nav.style.boxShadow = "0 5px 15px rgba(92, 92, 92, 0.7)"
}