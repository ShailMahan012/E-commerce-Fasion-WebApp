var all_products = []

// Check if products key exist in localStorage or not
if (!localStorage.getItem("products")) {
    localStorage.setItem("products", '[]') // make products key with empty array
}

function get_products() {
    var products = JSON.parse(localStorage.getItem("products"))
    return products
}


function add_to_cart(id, quantity) {
    var products = get_products()
    if (find_product_id(products, id) === false)
        products.push({id:id, quantity:quantity})
    localStorage.setItem("products", JSON.stringify(products))
    console.log(products)
}


function remove_from_cart(id) {
    var products = get_products()
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


function make_product(id, title, description, img, quantity, price) {
    var total = quantity * price
    var template = `
        <tr>
            <td class="img-cell">
                <img class="product-img" src="/static/${img}" alt="Hoodie">
            </td>
            <td class="info-cell">
                ${title}<br>
                ${description}<br>
                ${price}<br>
                <button class="clear-btn">clear</button>
            </td>
            <td class="quantity-cell">
                <button class="quantity-btn">-</button>
                <input type="text" name="quantity" id="quantity" value="${price}">
                <button class="quantity-btn">+</button>
            </td>
            <td class="total-cell">
                ${total}
            </td>
        </tr>
    `
    return template
}


function fetch_products() {
    let products = get_products()
    let products_id = []
    for(let i=0;i<products.length;i++) {
        products_id.push(products[i].id)
    }
    if (products_id.length) {
        products_id = JSON.stringify(products_id) // + "a"
        $.post("/fetch/products", { id: products_id }, function (result) {
            console.log(result)
        })
    }
}