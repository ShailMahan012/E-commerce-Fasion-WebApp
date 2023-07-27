const f_name = get('f_name')
const l_name = get('l_name')
const email = get('email')
const address = get('address')
const city = get('city')
const postal_code = get('postal_code')
const phone = get('phone')
const URL = "/checkout"


const inputs = {
    f_name: f_name,
    l_name: l_name,
    email,
    address,
    city,
    postal_code,
    phone
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
            return result.text()
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

var form = gen_order_form()
if (form != -1) {
    send_data(form, URL).then(result=> {
        console.log(result)
    })
}

