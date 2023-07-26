var images = document.getElementsByClassName("img")
var img_search_input = get("img_search_input")
var popup = document.getElementById("popup")
var overlay = get("overlay")
var search_div = document.getElementById("search_div")


function img_select(img_id) {
    show_popup()
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


function create_row(img_id) {

}


function show_images() {
    let search = img_search_input.value
    if (search) {
        fetch_images(search).then(result=> {
            console.log(result)
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

img_search_input.onkeydown = show_images