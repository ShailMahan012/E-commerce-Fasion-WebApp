const tbody_prooducts = get('products')
const total_price = get('total_price')


// Check if products key exist in localStorage or not
if (!localStorage.getItem("products")) {
    localStorage.setItem("products", '[]') // make products key with empty array
}


function save_products(products) {
    localStorage.setItem("products", JSON.stringify(products))
}


function add_to_cart(id, quantity) {
    let products = get_products()
    if (find_product(products, id) === -1) // if not found then store it
        products.push({id:id, quantity:quantity})
    save_products(products)
    cart_indicator_update() // main.js
}


// Remove product from localStorage
function remove_from_cart(id) {
    let products = get_products()
    let i = find_product(products, id)
    if (i != -1) {
        products.splice(i, 1)
        save_products(products)
    }
    cart_indicator_update() // main.js
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
    let prd_quantity = get("quantity_" + id)
    let prd_quantity_m = get("quantity-m_" + id) // Mobile version of quantity input

    prd_id = find_product(products, id)
    let quantity = products[prd_id].quantity += i
    if (quantity<1) return null
    prd_quantity.value = quantity
    prd_quantity_m.value = quantity
    save_products(products)
    update_prices()
}


// Update prices of each product with respect to quantity also total price of all products
function update_prices() {
    let products = get_products() // get all products stored in localStorage
    let total = 0
    for (let i=0;i<products.length;i++) {
        let prd = products[i]
        let discount = prd.discount
        let prd_price_node = get("price_" + prd.id) // Get element where price of current product is stored
        let prd_price = prd.quantity * prd.price
        if (discount) prd_price = prd_price * (100-discount) / 100
        prd_price_node.innerText = prd_price // update net price in table column for specific product
        total += prd_price
    }
    total_price.innerText = total * (100-discount) / 100// Update total price of all elements
}


// remove row of product as well as from localStorage
function delete_product(id) {
    var prd_node = get("product_" + id)
    if (prd_node) {
        remove_from_cart(id)
        prd_node.remove()
        update_prices()
    }
}


function make_product(prd, net_price) {
    if (!prd.discount) prd.discount = 0
    let template = `
        <tr id="product_${prd.id}">
            <td class="img-cell">
                <a href="/product/${prd.id}">
                <img class="product-img" src="/static/product_images/${prd.img}" alt="${prd.title}">
                </a>
            </td>
            <td class="info-cell">
                <a href="/product/${prd.id}">
                ${prd.title}<br>
                \$${prd.price}<br>
                </a>
                <div class="quantity-mobile">
                    <button class="quantity-btn" onclick="update_quantity(${prd.id}, -1)">-</button>
                    <input type="text" name="quantity" class="quantity" id="quantity-m_${prd.id}" value="${prd.quantity}" disabled>
                    <button class="quantity-btn" onclick="update_quantity(${prd.id}, 1)">+</button>
                </div>
                <div class="discount-mobile">Discount: ${prd.discount}%</div>
                <button class="clear-btn" onclick="delete_product(${prd.id})">remove</button>
            </td>
            <td class="discount-cell">${prd.discount}%</td>
            <td class="quantity-cell">
                <button class="quantity-btn" onclick="update_quantity(${prd.id}, -1)">-</button>
                <input type="text" name="quantity" class="quantity" id="quantity_${prd.id}" value="${prd.quantity}" disabled>
                <button class="quantity-btn" onclick="update_quantity(${prd.id}, 1)">+</button>
            </td>
            <td class="total-cell" id="price_${prd.id}">
                \$${net_price}
            </td>
        </tr>
    `
    return template
}


function display_products(all_products) {
    let total_products_price = 0

    tbody_prooducts.innerHTML = '<tr style="height: 10px;"></tr>' // createing tr just for some margin at top

    for (let i=0;i<all_products.length;i++) {
        let prd = all_products[i]
        let net_price = prd.price * prd.quantity
        if (prd.discount) {
            net_price = net_price * (100 - prd.discount) / 100
        }
        total_products_price += net_price
        let product = make_product(prd, net_price)
        tbody_prooducts.innerHTML += product
    }

    total_price.innerText = total_products_price * (100-discount) / 100
}


function fetch_products() {
    let products = get_products() // localStorage Products
    let products_id = [] // store cart products id in it and send it to api
    let products_quantity = {} // quantity of every product
    let all_products = [] // array of all products with all data to display to client
    for(let i=0;i<products.length;i++) {
        let prd = products[i]
        products_id.push(prd.id)
        products_quantity[prd.id] = prd.quantity
    }

    if (products_id.length) {
        products_id = JSON.stringify(products_id)
        $.post("/fetch/products", { id: products_id }, function (result) {
            // result is json array returned by server which contains data of all products availabe in cart
            for (let i=0;i<result.length-1;i++) {
                let prd = result[i] // Get i element of product from given by server using API
                prd['quantity'] = products_quantity[prd.id]
                let localStorage_prd = products[find_product(products, prd.id)] // Get product with prd.id
                localStorage_prd.price = prd.price // add or update price of products in localStorage

                localStorage_prd.discount = prd.discount
                all_products.push(prd)
            }
            display_products(all_products) // Display all products in table
            save_products(products) // Update products in localStorage
        })
    }
}

