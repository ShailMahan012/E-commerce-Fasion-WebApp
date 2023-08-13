const sub = get("sub-container")

function show_sub() {
    overlay.style.display = "block"
    setTimeout(()=> {
        overlay.style.opacity = "1"
        sub.style.top = "10%"
    }, 1000)

}

function hide_sub() {
    sub.style.top = "-100%"
    overlay.style.opacity = "0"
    setTimeout(()=>{
        overlay.style.display = "none"
    }, 1000)
}
