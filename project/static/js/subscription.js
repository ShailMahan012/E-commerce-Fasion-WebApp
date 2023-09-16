const sub = get("sub-container")
const sub_email = get("sub-email")
const sub_thanks = get("sub-thanks")

function subscribe() {
    let email = sub_email.value
    if (email && sub_email.checkValidity()) {
        fetch(`/subscribe?email=${email}`).then(resp => { return resp.text() }).then(resp => {
            console.log("SUBSCRIPTION: " + resp)
        }).catch((err)=> {
            console.log(err)
        })
        subscription_done()
    }
    else {
        console.log("Email Validity Error")
    }
}


function subscription_done() {
    sub_thanks.style.display = "block"
    setTimeout(()=> {
        sub_thanks.style.top = "0"
    }, 100)
    sub_email.value = ""
}

function sub_thanks_close() {
    sub_thanks.style.top = "-100%";
    sub_thanks.addEventListener("transitionend", ()=> {
        sub_thanks.style.display = "none"
    }, {once: true})
}
