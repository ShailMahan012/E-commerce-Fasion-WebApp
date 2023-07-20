var f_name = document.getElementById('f_name')
var l_name = document.getElementById('l_name')
var email = document.getElementById('email')
var address = document.getElementById('address')
var city = document.getElementById('city')
var postal_code = document.getElementById('postal_code')
var phone = document.getElementById('phone')



function get_products() {
    let products = JSON.parse(localStorage.getItem("products"))
    return products
}

