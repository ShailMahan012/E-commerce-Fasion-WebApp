var search = document.getElementById("search")
var header = document.getElementById("header")
var nav = document.getElementById("nav")
var search_input = document.getElementById("search_input")

function show_search() {
    search.style.transform = "translateY(0)"
    // setTimeout(()=> {search.style.zIndex = 0}, 1000)
    search.style.zIndex = 100
    nav.style.boxShadow = "none"
    setTimeout(()=> {search_input.focus()}, 700)
}


function hide_search() {
    const zIndexPromise = new Promise((resolve) => {
        search.style.zIndex = '98';
        resolve();
    });
    zIndexPromise.then(function () {
        search.style.transform = "translateY(-70px)"
        // search.style.visibility = "hidden"
        nav.style.boxShadow = "0 5px 15px rgba(92, 92, 92, 0.7)"
    })
}

function toggleNav() {
    alert(1)
}