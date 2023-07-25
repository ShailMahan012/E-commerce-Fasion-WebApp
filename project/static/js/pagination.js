function page_go(num) {
    if (num != "None")
        window.location.href = `/search/${num}?search_input=${searched}`
}