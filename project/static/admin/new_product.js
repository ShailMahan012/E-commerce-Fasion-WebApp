var images = document.getElementsByClassName("img")
var img_search_input = get("img_search_input")
var popup = document.getElementById("popup")
var overlay = get("overlay")
var search_div = document.getElementById("search_div")
var img_id = -1 // ID of image container in which we are going to place image -1 means no image container is select
var fetched_images;

function img_select() {
}


function img_del(file_img_id) {
    let img_file = image_file_input[file_img_id]
    let image = images[file_img_id]

    img_file.value = null
    if (!image.src.endsWith("#")) image.src = "#"
}


function img_change(file_img_id) {
    let img_file = image_file_input[file_img_id]
    let image = images[file_img_id]
    if (img_file.value) {
        image.src = URL.createObjectURL(img_file.files[0])
    }
    else {
        image.src = "#"
    }
}


function create_row(img_data, id) {
    let filename = img_data.filename
    let title = img_data.title
    let row = `
        <div class="search_row" onclick(img_select(${id}))>
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
            fetched_images = result
            for (let i=0;i<result.length;i++) {
                let row = create_row(result[i], i)
                search_div.innerHTML += row
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
