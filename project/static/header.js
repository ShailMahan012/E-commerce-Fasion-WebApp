var search = document.getElementById("search")
var header = document.getElementById("header")
var nav = document.getElementById("nav")
var nav2 = document.getElementById("nav2")
var search_input = document.getElementById("search_input")
var container = document.getElementById("container")

function after_load() {
    container.style.top = nav2.clientHeight + "px"
}


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
    // Navbar is closed if top is not 0px
    if (nav.style.top != "0px") {
        // Show NAV
        nav.style.top = "0px"
        container.style.top = "0px"
        setTimeout(()=>{nav.style.position = "relative"}, 510)
    }
    else {
        // Hide NAV
        nav.style.top = "-300px"
        nav.style.position = "absolute"
        container.style.top = nav2.clientHeight + "px"
        // Also hide search just in case if it might be opened. It just look ugly when nav is closed and search is still showing
        hide_search()
    }
}