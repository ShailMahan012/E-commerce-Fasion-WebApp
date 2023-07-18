var tbody_prooducts = document.getElementById('products')
var total_price = document.getElementById('total_price')
var all_products = []

// Check if products key exist in localStorage or not
if (!localStorage.getItem("products")) {
    localStorage.setItem("products", '[]') // make products key with empty array
}

function get_products() {
    let products = JSON.parse(localStorage.getItem("products"))
    return products
}


function save_products(products) {
    localStorage.setItem("products", JSON.stringify(products))
}


function add_to_cart(id, quantity) {
    let products = get_products()
    if (find_product(products, id) === -1) // if not found then store it
        products.push({id:id, quantity:quantity})
    save_products(products)
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
}


function find_product(products, id) {
    for (let i=0;i<products.length;i++) {
        if (products[i].id === id)
            return i // found
    }
    return -1 // not found
}


function update_quantity(id, i) {
    let products = get_products()
    let prd_quantity = document.getElementById("quantity_" + id)
    prd_id = find_product(products, id)
    let quantity = products[prd_id].quantity += i
    if (quantity<1) return null
    prd_quantity.value = quantity
    save_products(products)
}


function make_product(prd, net_price) {
    var template = `
        <tr>
            <td class="img-cell">
                <img class="product-img" src="/static/product_images/${prd.img}" alt="${prd.title}">
            </td>
            <td class="info-cell">
                ${prd.title}<br>
                ${prd.price}<br>
                <button class="clear-btn">clear</button>
            </td>
            <td class="quantity-cell">
                <button class="quantity-btn" onclick="update_quantity(${prd.id}, -1)">-</button>
                <input type="text" name="quantity" class="quantity" id="quantity_${prd.id}" value="${prd.quantity}" disabled>
                <button class="quantity-btn" onclick="update_quantity(${prd.id}, 1)">+</button>
            </td>
            <td class="total-cell">
                ${net_price}
            </td>
        </tr>
    `
    return template
}


function display_products() {
    let total_products_price = 0

    tbody_prooducts.innerHTML = '<tr style="height: 10px;"></tr>' // createing tr just for some margin at top

    for (let i=0;i<all_products.length;i++) {
        let prd = all_products[i]
        let net_price = prd.price * prd.quantity
        total_products_price += net_price
        let product = make_product(prd, net_price)
        tbody_prooducts.innerHTML += product
    }

    total_price.innerText = total_products_price
}


function fetch_products() {
    let products = get_products()
    let products_id = [] // store cart products id in it and  send it to api
    let products_quantity = {} // quantity of every product
    all_products = [] // empty all_products arraay
    for(let i=0;i<products.length;i++) {
        let prd = products[i]
        products_id.push(prd.id)
        products_quantity[prd.id] = prd.quantity
    }

    if (products_id.length) {
        products_id = JSON.stringify(products_id)
        $.post("/fetch/products", { id: products_id }, function (result) {
            // result is json array returned by server which contains data of all products availabe in cart
            for (let i=0;i<result.length;i++) {
                let prd = result[i]
                prd['quantity'] = products_quantity[prd.id]
                all_products.push(prd)
            }
            display_products()
        })
    }
}

