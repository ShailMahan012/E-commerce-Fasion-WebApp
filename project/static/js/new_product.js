var image_file_input = document.getElementsByClassName("img_file")
var images = document.getElementsByClassName("img")


function upload(file_img_id) {
    image_file_input[file_img_id].click()
}


function del_image(file_img_id) {

}


function img_change(file_img_id) {
    console.log("img_change")
    let img_file = image_file_input[file_img_id]
    images[file_img_id].src = URL.createObjectURL(img_file.files[0])
}