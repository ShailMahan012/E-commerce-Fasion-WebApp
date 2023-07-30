const orders = get("orders")
const popup = get("popup")
const overlay = get("overlay")


function display_orders() {
    orders.innerHTML = ''
    let i = 1
    for (let [_, value] of Object.entries(orders_json)) {
        let row = create_row(i++, value)
        orders.innerHTML += row
    }
}

display_orders()

function create_row(i, order) {
    let price = calc_price(order)
    let row = `
        <tr>
            <td>${i}</td>
            <td>${order.f_name} ${order.l_name}</td>
            <td>${order.note}</td>
            <td>${price}</td>
            <td>${order.status}</td>
        </tr>
    `
    return row
}


function calc_price(order) {
    let price = 0
    let items = order.items
    for (let i=0;i<items.length;i++) {
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
        popup.style.top = "100px"
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
