const orders = get("orders") // tbody of orders
const products = get("products") // tbody of pop
const order_id = get("ord_id") // order id in popup
const not_found = get("not_found") // not found message in popup
const total_price = get("total_price") // total price of full order in popup
const popup = get("popup")
const overlay = get("overlay")


const name = get("name")
const phone = get("phone")
const address = get("address")
const city = get("city")
const postal_code = get("postal_code")
const note = get("note")


// Display all orders in different rows of table
function display_orders() {
    orders.innerHTML = ''
    let i = 1
    for (let [ord_id, value] of Object.entries(orders_json)) {
        let row = create_order_row(i++, value, ord_id)
        orders.innerHTML += row
    }
}
display_orders()


// Show only one order details with all products (image, quantity, price, total price with quantity)
function show_order(ord_id) {
    products.innerHTML = ''
    let order = orders_json[ord_id] // get specific order with its id
    let items = order.items // get all products/items of that order
    let ord_total_price = 0
    order_id.innerText = ord_id // show order id in popup

    for(let i=0;i<items.length;i++) {
        let prd_id = items[i].product
        prd = products_json[prd_id] // get one product
        let quantity = items[i].quantity
        let prd_total_price = quantity * prd.price
        ord_total_price += prd_total_price
        let row = create_product_row(i+1, prd, quantity, prd_total_price) // create row of that one product
        products.innerHTML += row
    }

    
    if (items.length === 0) not_found.style.display = "block"
    else not_found.style.display = "none"
    set_order_data(order, ord_total_price)
    show_popup()
}


// create one row of product in popup
function create_product_row(i, prd, quantity, total_price) {
    let image_url = prd.images[0].filename
    row = `
        <tr>
            <td>${i}</td>
            <td><img alt='IMAGE' class='img' src='/static/product_images/${image_url}'></td>
            <td>${prd.title}</td>
            <td class="category">${prd.category}</td>
            <td>${prd.price}</td>
            <td>${quantity}</td>
            <td>${total_price}</td>
        </tr>
    `
    return row
}


function set_order_data(order, ord_total_price) {
    name.innerText = order.f_name + ' ' + order.l_name
    phone.innerText = order.phone
    address.innerText = order.address
    city.innerText = order.city
    postal_code.innerText = order.postal_code
    note.innerText = order.note
    total_price.innerText = ord_total_price
}


// create one order row
function create_order_row(i, order, ord_id) {
    let price = calc_price(order)
    let row = `
        <tr onclick="show_order(${ord_id})">
            <td>${i}</td>
            <td>${order.f_name} ${order.l_name}</td>
            <td>${order.note}</td>
            <td>${price}</td>
            <td>${order.status}</td>
        </tr>
    `
    return row
}


// calculate total price of specific order
function calc_price(order) {
    let price = 0
    let items = order.items // all products of that order
    for (let i=0;i<items.length;i++) { // iterate over products
        let item = items[i]
        let quantity = item.quantity
        let product = products_json[item.product]
        price += quantity * product.price
    }
    return price
}


function show_popup() {
    popup.style.display = 'block'
    overlay.style.display = 'block'
    popup.style.transitionDelay = '200ms'
    overlay.style.transitionDelay = '0ms'
    setTimeout(()=>{
        popup.style.top = "50px"
        overlay.style.opacity = 1
    }, 100)
}


function hide_popup() {
    popup.style.transitionDelay = '0ms'
    overlay.style.transitionDelay = '700ms'
    setTimeout(()=> {
        popup.style.top = "-100%"
        overlay.style.opacity = 0
    }, 100)
    setTimeout(()=> {
        popup.style.display = 'none'
        overlay.style.display = 'none'
    }, 1000)
}
