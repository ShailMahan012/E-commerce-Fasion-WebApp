function get_products() {
    let products = JSON.parse(localStorage.getItem("products"))
    return products
}

function cart_indicator_update() {
    const cart_indicator = get("cart-indicator")

    let products = get_products()
    if (products == null) products = []
    cart_indicator.innerHTML = products.length
}
