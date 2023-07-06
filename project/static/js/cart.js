// Check if products key exist in localStorage or not
if (!localStorage.getItem("products")) {
    localStorage.setItem("products", '[]') // make products key with empty array
}

function add_to_cart(id, quantity) {
    var products = JSON.parse(localStorage.getItem("products"))
    products.push({id:id, quantity:quantity})
    console.log(products)
    localStorage.setItem("products", JSON.stringify(products))
}
