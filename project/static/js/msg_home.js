const msg_div = get("msg_div")

// Show message with message and alert type like danger, primary and warning etc
function msg(m, type) {
    msg_div.innerHTML = m
    msg_div.className = "alert-home alert alert-" + type
    msg_div.style.right = "30px"
    setTimeout(()=> {hide_msg()}, 5000)
}


// Just hide msg div
function hide_msg() {
    msg_div.style.right = "-100%"
}
