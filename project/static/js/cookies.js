const cookies = get("cookies")


function check_cookies() {
    let cookies = localStorage.getItem("cookies")
    if (!cookies) {
        show_cookies()
    }
}


function show_cookies() {
    overlay.style.display = "block"
    cookies.style.display = "block"
    setTimeout(()=>{
        overlay.style.opacity = 1
        cookies.style.bottom = "1px"
    }, 500)
}


function hide_cookies() {
    localStorage.setItem("cookies", "true")

    overlay.style.opacity = 0
    cookies.style.bottom = "-400px"

    setTimeout(()=>{
        overlay.style.display = "none"
        cookies.style.display = "none"
    }, 500)
}


setTimeout(check_cookies, 3000)
