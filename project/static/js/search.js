const searched_prd = get("searched-product-row")
var searching = false;


async function search_prd() {
    let input = search_input.value.trim()
    if (input) {
        let products = await fetch_searched_products(input)
        searched_prd.innerHTML = ""
        for(let i=0;i<products.length;i++) {
            show_searched_product(products[i])
        }
    }
}

function show_searched_product(prd) {
    let one_prd = `
    <div class="column">
        <div class="searched-product" onclick="go('/product/${prd.id}')">
            <img class="searched-product-img" src="/static/product_images/${prd.img}" alt="">
            <div class="searched-product-title">${prd.title}</div>
        </div>
    </div>`
    searched_prd.innerHTML += one_prd
}

async function fetch_searched_products(input) {
    return await fetch(`/search/products?search_input=${input}`)
    .then(result=>{return result.json()})
    .then(result=>{
        return result
    })
}

search_input.onkeyup = search_prd
