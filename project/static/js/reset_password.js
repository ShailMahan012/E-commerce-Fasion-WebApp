const email = get("email")
const code = get("code")
const passwords = document.querySelectorAll("input[type=password]")
const password = get("password")
const submit_btn = get("submit_btn")


async function submit_email() {
    msg("Please Wait!", "warning")
    submit_btn.disabled = true
    let email_addr = email.value.trim()
    if (email_addr) {
        let mail_code = Math.floor(Math.random() * 999999) + 100000;
        localStorage.setItem("mail_code", mail_code)
        var result = await submit_data({"email": {"email": email_addr, "code": mail_code}})
        if (result == "true") {
            msg("Email with code has been sent", "primary")
            email.style.display = "none"
            code.style.display = "block"
            submit_btn.innerText = "Verify"
            submit_btn.onclick = verify_code
        }
        else if (result == "Not Found") {
            msg("Email Not Found!", "danger")
        }
        else {
            msg("Something went wrong", "danger")
        }
    }
    submit_btn.disabled = false
}

function verify_code() {
    let mail_code = localStorage.getItem("mail_code")
    if (mail_code) {
        if (code.value == mail_code) {
            msg("Enter New Password", "primary")
            code.style.display = "none"
            passwords[0].style.display = "block"
            passwords[1].style.display = "block"
            submit_btn.innerText = "Change Password"
            submit_btn.onclick = submit_password
        }
        else {
            msg("Wrong Code", "danger")
        }
    }
    else
    window.location.reload()
}

async function submit_password() {
    if (passwords[0].value == passwords[1].value) {
        let result = await submit_data({"password": {"email": email.value, "password": passwords[0].value}})
        console.log(result)
        if (result == "true") {
            msg("Password Changed Successfully")
            submit_btn.style.display = "none"
            passwords[0].style.display = "none"
            passwords[1].style.display = "none"
        }
        else {
            msg("Something Went Wrong!", "danger")
        }
    }
    else {
        msg("Enter same passwords", "danger")
        passwords[0].focus()
    }
}


async function submit_data(data) {
    return await fetch(`/user/reset_password`
        , {
            method: "POST",
            "headers": { "Content-Type": "application/json" },
            "body": JSON.stringify(data),
        }
    )
    .then(result=>{
        return result.text()
    })
}

