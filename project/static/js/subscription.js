const sub = get("sub-container")
const sub_email = get("sub-email")

function subscribe() {
    let email = sub_email.value
    if (email && sub_email.checkValidity()) {
        fetch(`/subscribe?email=${email}`).then(resp => { return resp.text() }).then(resp => {
            // subscription_done()
        })
    }
    else {
        console.log("False")
    }
}

