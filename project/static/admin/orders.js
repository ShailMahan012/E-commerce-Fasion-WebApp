const orders = get("orders") // tbody of orders
const products = get("products") // tbody of pop
const order_id = get("ord_id") // order id in popup
const not_found = get("not_found") // not found message in popup
const popup = get("popup")
const overlay = get("overlay")
const btn_order_status = get("btn_order_status") // button to mark order as completed

const name = get("name")
const phone = get("phone")
const address = get("address")
const city = get("city")
const postal_code = get("postal_code")
const note = get("note")
const status = get("status")
const date = get("date")
const total_price = get("total_price") // total price of full order in popup

var current_order_id = -1; // GLOBAL variable to be used to mark order

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
    current_order_id = ord_id
    products.innerHTML = ''
    let order = orders_json[ord_id] // get specific order with its id
    let items = order.items // get all products/items of that order
    let ord_total_price = 0
    order_id.innerText = ord_id // show order id in popup

    for(let i=0;i<items.length;i++) {
        let item = items[i]
        let images = images_json[item.product] // get images of that item
        let quantity = item.quantity
        let prd_total_price = quantity * item.price
        ord_total_price += prd_total_price
        let row = create_product_row(i+1, images, item, quantity, prd_total_price) // create row of that one product
        products.innerHTML += row
    }

    
    if (items.length === 0) not_found.style.display = "block"
    else not_found.style.display = "none"
    set_order_data(order, ord_total_price)
    show_popup()
}


// create one row of product in popup
function create_product_row(i, images, item, quantity, total_price) {
    let image_url = "not-found.png"
    if (images.length != 0)
        image_url = images[0].filename
    row = `
        <tr>
            <td>${i}</td>
            <td><img alt='IMAGE' class='img' src='/static/product_images/${image_url}'></td>
            <td>${item.title}</td>
            <td>${item.price}</td>
            <td>${quantity}</td>
            <td>${total_price}</td>
        </tr>
    `
            // <td class="category">${item.category}</td>
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
    date.innerText = order.date
    
    let status_txt = "PENDING"
    let btn_status = "Mark As Completed"
    if (order.status) {
        status_txt = "COMPLETED"
        btn_status = "Mark As Uncompleted"
    }
    status.innerText = status_txt
    btn_order_status.innerText = btn_status
}


// create one order row
function create_order_row(i, order, ord_id) {
    let price = calc_price(order)
    let status_td = "<td class='status pending'>PENDING</td>"
    if (order.status) status_td = "<td class='status done'>COMPLETED</td>"
    let row = `
        <tr onclick="show_order(${ord_id})">
            <td>${i}</td>
            <td>${order.f_name} ${order.l_name}</td>
            <td>${order.note}</td>
            <td>${price}</td>
            <td>${order.date}</td>
            ${status_td}
        </tr>
    `
    return row
}


// calculate total price of specific order
function calc_price(order) {
    let total_price = 0
    let items = order.items // all products of that order
    for (let i=0;i<items.length;i++) { // iterate over products
        let item = items[i]
        let quantity = item.quantity
        let price = item.price
        total_price += quantity * price
    }
    return total_price
}


function mark_order() {
    if (current_order_id != -1) {
        go(`/admin/order/mark/${current_order_id}/${page_num}`)
    }
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
