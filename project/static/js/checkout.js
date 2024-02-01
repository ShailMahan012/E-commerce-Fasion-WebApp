const f_name = get('f_name')
const l_name = get('l_name')
const email = get('email')
const address = get('address')
const city = get('city')
const country = get('country')
const postal_code = get('postal_code')
const phone = get('phone')
const note = get('note')
const CHECKOUT_URL = "/checkout"

const paypal_container = get("paypal-button-container")

const inputs = {
    f_name: f_name,
    l_name: l_name,
    email: email,
    address: address,
    city: city,
    country: country,
    postal_code: postal_code,
    phone: phone,
    note: note
}

function checkout() {
    if (validate_form()) {
        show_paypal()
    }
}

function validate_form() {
    for (const key in inputs) {
        let input = inputs[key];
        if (key == "country") {
            if (!input.value) {
                msg("Select Your Country", "danger")
                return false
            }
        }
        else if (!input.checkValidity()) {
            input.reportValidity();
            console.log("VALIDITY ISSUE: ", input)
            return false;
        }
    }
    return true
}

function get_products() {
    let products = JSON.parse(localStorage.getItem("products"))
    return products
}

function gen_order_form() {
    let products = localStorage.getItem("products")
    if (!products) return -1
    let form = new FormData();
    
    for(const key in inputs) {
        let input = inputs[key];
        form.append(key, input.value)
    }
    form.append("products", products)
    return form
}

async function send_data(form, url) {
    var output = "false";

    await fetch(url, {
        method: "POST",
        body: form,
    })
        .then((result) => {
            return result.json()
        })
        .then(text => {
            output = text
        })
        .catch((error) => {
            console.log(error)
            output  = "error";
        })
    return output;
}

function show_paypal() {
    overlay.style.display = "block"
    paypal_container.style.display = null
    setTimeout(()=> {
        overlay.style.opacity = "1"
        paypal_container.style.top = "10px"
        paypal_container.style.bottom = "0"
    }, 200)
    
}

function hide_paypal() {
    overlay.style.opacity = "0"
    paypal_container.style.top = null
    paypal_container.style.bottom = null
    setTimeout(()=> {
        paypal_container.style.display = "none"
        overlay.style.display = "none"
    }, 200)
    
}

overlay.onclick = hide_paypal
