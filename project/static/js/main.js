const msg_div = document.getElementById("msg_div")

// Show message with message and alert type like danger, primary and warning etc
function msg(m, type) {
    msg_div.style.display = "block"

    msg_div.innerHTML = m
    msg_div.className = "alert alert-" + type
}


// Just hide msg div
function hide_msg() {
    msg_div.style.display = "none"
}


function get_products() {
    let products = JSON.parse(localStorage.getItem("products"))
    return products
}

function cart_indicator_update() {
    const cart_indicator = document.getElementById("cart-indicator")
    let products = get_products()
    if (products == null) products = []
    cart_indicator.innerHTML = products.length
}
