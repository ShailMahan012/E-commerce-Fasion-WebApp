function get(id) {
    return document.getElementById(id)
}

var search = get("search")
var header = get("header")
var nav = get("nav")
var nav2 = get("nav2")
var search_input = get("search_input")
var container = get("container")
var btn_toggle_nav = get("btn-toggle-nav")

function after_load() {
    // container.style.top = nav2.clientHeight + "px"
    container.style.marginTop = nav2.clientHeight + "px"
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
        btn_toggle_nav.classList.add("nav-show-rotate")
        setTimeout(()=>{btn_toggle_nav.classList.remove("nav-show-rotate")}, 1020)

        // Show NAV
        nav.style.top = "0px"
        // container.style.top = "0px"
        container.style.marginTop = "0px"
        setTimeout(()=>{nav.style.position = "relative"}, 510)
    }
    else {
        btn_toggle_nav.classList.add("nav-hide-rotate")
        setTimeout(()=>{btn_toggle_nav.classList.remove("nav-hide-rotate")}, 1020)

        // Also hide search just in case if it might be opened. It just look ugly when nav is closed and search is still showing
        hide_search()
        // Hide NAV
        nav.style.top = "-300px"
        nav.style.position = "absolute"
        setTimeout(()=>{nav.style.position = "absolute"}, 510)
        // container.style.top = nav2.clientHeight + "px"
        container.style.marginTop = nav2.clientHeight + "px"
    }
}

function go(url) {
    window.location.href = url
}
