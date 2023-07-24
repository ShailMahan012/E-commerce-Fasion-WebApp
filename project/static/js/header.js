function get(id) {
    return document.getElementById(id)
}

var search = get("search")
var header = get("header")
var nav = get("nav")
var nav2 = get("nav2")
var nav_show = false
var search_input = get("search_input")
var search_show = false
var container = get("container")
var btn_toggle_nav = get("btn-toggle-nav")

function after_load() {
    container.style.marginTop = nav2.clientHeight + "px"
    pos_search()
}


function show_search() {
    search_show = true
    pos_search()
    // setTimeout(()=> {search.style.zIndex = 0}, 1000)
    search.style.zIndex = 100
    nav.style.boxShadow = "none"
    nav2.style.boxShadow = "none"
    setTimeout(()=> {search_input.focus()}, 700)
}


function hide_search() {
    search_show = false
    const zIndexPromise = new Promise((resolve) => {
        search.style.zIndex = '98';
        resolve();
    });
    // wait for z-index to change
    zIndexPromise.then(function () {
        pos_search()
        nav.style.boxShadow = "0 5px 15px rgba(92, 92, 92, 0.7)"
    })
}


function pos_search() {
    let top;

    // nav2 height is 0. Which means nav2 is hidden and there is no toggling navbar
    if (nav2.clientHeight === 0) {
        if (search_show) {
            top = 0
        }
        else {
            top = -nav.clientHeight
        }
    }
    else {
        // if nav is going to open then set search box right bellow the opened navbar
        if (nav_show) {
            if (search_show) {
                top = nav.clientHeight - nav2.clientHeight
            }
            else {
                top = nav.clientHeight - nav2.clientHeight - search.clientHeight
            }
        }
        // if nav is going to close then set search box position with negative navbar height so that it will completely hidden
        else {
            top = -nav2.clientHeight
        }
    }
    search.style.transform = `translateY(${top}px)`
}


function toggleNav() {
    // Navbar is closed if top is not 0px
    // Show NAVBAR
    if (nav.style.top != "0px") {
        nav_show = true
        btn_toggle_nav.classList.add("nav-show-rotate")
        setTimeout(()=>{btn_toggle_nav.classList.remove("nav-show-rotate")}, 1020)

        // Show NAV
        nav.style.top = "0px"
        nav2.style.boxShadow = "none"
        hide_search()
        // container.style.top = "0px"
        // container.style.marginTop = "0px"
        // setTimeout(()=>{nav.style.position = "relative"}, 510)
    }
    // HIDE NAVBAR
    else {
        nav_show = false
        btn_toggle_nav.classList.add("nav-hide-rotate")
        setTimeout(()=>{
            btn_toggle_nav.classList.remove("nav-hide-rotate")
        }, 1020)

        // Also hide search just in case if it might be opened. It just look ugly when nav is closed and search is still showing
        hide_search()
        // Hide NAV
        nav.style.top = "-300px"
        nav.style.position = "absolute"
        nav2.style.boxShadow = "0 5px 15px rgba(92, 92, 92, 0.7)"
        setTimeout(()=>{nav.style.position = "absolute"}, 510)
        // container.style.top = nav2.clientHeight + "px"
        // container.style.marginTop = nav2.clientHeight + "px"
    }
}

function go(url) {
    window.location.href = url
}

