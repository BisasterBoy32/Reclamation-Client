
const usernameError = document.querySelector("#u-error")
const emailError = document.querySelector("#e-error") 
const pass1Error1 = document.querySelector("#p1-error1") 
const pass1Error2 = document.querySelector("#p1-error2") 
const pass1Error3 = document.querySelector("#p1-error3") 
const pass2Error = document.querySelector("#p2-error")  
const phoneError = document.querySelector("#t-error") 

const errors = [usernameError, emailError, pass1Error1, pass1Error2, pass1Error3, pass2Error, phoneError]

const username = document.querySelector("#username")
const email = document.querySelector("#email")
const pass1 = document.querySelector("#pass1")
const pass2 = document.querySelector("#pass2")
const phone = document.querySelector("#phone")
const btn = document.querySelector("#btn")

// regex for alphabitic and numbers
const alph = /^(?=.*[a-z]).+$/
const numbers = /^(?=.*[0-9_\W]).+$/

// the password validation
pass1.addEventListener("input",function(e){
    // check if the pasword more than 8 chars
    console.log(e.target.value)
    if ( this.value.length < 8 ){
        pass1Error2.classList.add("not-valid")
    }else{
        pass1Error2.classList.replace("not-valid","valid")
    }
    // check if the pasword contains chars and numbers
    if (this.value.match(alph) === null || this.value.match(numbers) === null ) {
        pass1Error1.classList.add("not-valid")
    }else {
        pass1Error1.classList.replace("not-valid","valid")
    }
    // check if the pasword diffrent than the username
    if (this.value.includes(username.value) ){
        pass1Error3.classList.add("not-valid")
    }else {
        pass1Error3.classList.replace("not-valid","valid")
    }
})

pass2.addEventListener("input",function(){
    if (this.value !== pass1.value ){
        pass2Error.classList.add("not-valid")
    }else {
        pass2Error.classList.replace("not-valid", "valid")
    }
})


// the username validation
username.addEventListener("input" , function(){
    const usern = this.value
    const url = `../username_valid/${usern}/`

    $.ajax({
        url: url,
        type: "GET",
        success: function(data){
            if (data.not_valid === true ){
                usernameError.classList.add("not-valid")
            }else {
                usernameError.classList.replace("not-valid","valid")
            }
        },
        error: function(errors){
            console.log("errors")
        }

    })
})

// the username validation
email.addEventListener("input", function () {
    const u_email = this.value
    const url = `../email_valid/${u_email}/`

    $.ajax({
        url: url,
        type: "GET",
        success: function (data) {
            if (data.not_valid === true) {
                emailError.classList.add("not-valid")
            } else {
                emailError.classList.replace("not-valid", "valid")
            }
        },
        error: function (errors) {
            console.log("errors")
        }

    })
})

//the  phone validation
phone.addEventListener("input" , function(){
    if ( this.value.length !== 9 || this.value[0] != 0){

        phoneError.classList.add("not-valid")
    }else {
        phoneError.classList.replace("not-valid","valid")
    }
})

// prevent the submit until all the inputs  
document.querySelector("#user-form").addEventListener("submit",function(e){
    let bigError = document.querySelector("#big-error")   
    let therIsError = false
    errors.map(function(error){
        if (error.classList.contains("not-valid")) {
            therIsError = true
        }
    })

    if (therIsError === true ){
        e.preventDefault()
        console.log("errors")
        bigError.innerHTML = "assurez - vous que vos informations correspondent aux règles d'inscription"
        bigError.classList.add("big-error")
        $("#big-error").hide()
        $("#big-error").fadeIn(2000)
    }else{
        bigError.innerHTML = ""
        bigError.classList.remove("big-error")

    }
})
