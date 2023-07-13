// Check if products key exist in localStorage or not
if (!localStorage.getItem("products")) {
    localStorage.setItem("products", '[]') // make products key with empty array
}


function add_to_cart(id, quantity) {
    var products = JSON.parse(localStorage.getItem("products"))
    if (find_product_id(products, id) === false)
        products.push({id:id, quantity:quantity})
    localStorage.setItem("products", JSON.stringify(products))
    console.log(products)
}


function remove_from_cart(id) {
    var products = JSON.parse(localStorage.getItem("products"))
    for (let i=0;i<products.length;i++) {
        if (id === products[i].id) {
            products.splice(i, 1)
            localStorage.setItem("products", JSON.stringify(products))
            break
        }
    }
    console.log(products)
}


function find_product_id(products, id) {
    for (let i=0;i<products.length;i++) {
        if (products[i].id === id)
            return true
    }
    return false
}
