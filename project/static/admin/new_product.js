var image_file_input = document.getElementsByClassName("img_file")
var img_div = document.getElementsByClassName("img_div")
var images = document.getElementsByClassName("img")


function upload(file_img_id) {
    image_file_input[file_img_id].click()
}


function del_image(file_img_id) {
    let img_file = image_file_input[file_img_id]
    let image = images[file_img_id]

    img_file.value = null
    image.src = "#"
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