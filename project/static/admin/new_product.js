const images = document.getElementsByClassName("img")
const images_ids = document.getElementsByClassName("img_id")
const img_search_input = get("img_search_input")
const popup = get("popup")
const overlay = get("overlay")
const search_div = get("search_div")

var img_id = -1 // ID of image container in which we are going to place image -1 means no image container is select
// var fetched_images;

// show images in img tag and also set value of input to image ID(IN DATABASE)
function img_select(id, filename) {
    let src = `/static/product_images/${filename}`
    let img_input = images_ids[img_id]
    img_input.value = id
    images[img_id].src = src
    hide_popup()
}


function img_del(img_id) {
    let img_input = images_ids[img_id]
    let image = images[img_id]

    img_input.value = null
    if (!image.src.endsWith("#")) image.src = "#"
}


function create_row(img_data) {
    let id = img_data.id
    let filename = img_data.filename
    let title = img_data.title
    let row = `
        <div class="search_row" onclick="img_select(${id}, '${filename}')">
            <img src="/static/product_images/${filename}" alt="img" class="img">
            <span>${title}</span>
        </div>`
    return row
}


function show_images() {
    let search = img_search_input.value
    search_div.innerHTML = ''
    if (search) {
        fetch_images(search).then(result=> {
            // fetched_images = result
            if (result.length > 0) {
                for (let i=0;i<result.length;i++) {
                    let row = create_row(result[i], i)
                    search_div.innerHTML += row
                }
            }
            else {
                search_div.innerHTML = `<span class="not-found">NOT FOUND</span>`
            }
        })
    }
}


function show_popup(id) {
    img_id = id
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
    img_id = -1
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


async function fetch_images(search) {
    var url = "/admin/fetch/images"
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
