const prd_search_input = get("prd_search_input")
const main_collection = get("main_collection")
const popup = get("popup")
const overlay = get("overlay")
const search_div = get("search_div")

var search_results = {}


function save_collection() {
    fetch("/admin/main_collection_home", {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(product_ids),
    }).then(result=> {
        msg("Data has been saved!", "primary")
    })
}


function prd_select(id) {
    let product = search_results[id]
    product_ids.push(id)
    let row = `
    <tr id="prd_${id}">
        <td>
            <img src="/static/product_images/${product.image}" alt="img" class="img">
        </td>
        <td>${product.title}</td>
        <td><button class="btn btn-del" onclick="prd_del(${id})">REMOVE</button></td>
    </tr>`
    main_collection.innerHTML += row
    hide_popup()
}


function prd_del(prd_id) {
    product_ids.pop(prd_id)
    let prd = get("prd_" + prd_id)
    prd.remove()
}


function create_row(id, prd_data) {
    let title = prd_data.title
    let image = prd_data.image
    let row = `
        <div class="search_row" onclick="prd_select(${id})">
            <img src="/static/product_images/${image}" alt="img" class="img">
            <span class="img-title">${title}</span>
        </div>`
    return row
}


function show_prd() {
    let search = prd_search_input.value
    search_div.innerHTML = ''
    if (search) {
        fetch_prd(search).then(result=> {
            search_results = result
            let prd_ids = Object.keys(result)
            if (prd_ids.length > 0) {
                for (let id in result) {
                    let row = create_row(id, result[id])
                    search_div.innerHTML += row
                }
            }
            else {
                search_div.innerHTML = `<span class="not-found">NOT FOUND</span>`
            }
        })
    }
}


function show_popup() {
    search_div.innerHTML = ''
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


async function fetch_prd(search) {
    var url = "/admin/fetch/products"
    var output = "false";
    let form = new FormData();
    form.append("search", search)
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
