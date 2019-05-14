const new_r = document.querySelector("#new-reclamation")
const noted_r = document.querySelector("#note")

newRec()
notedRec()

// get the number of new reclamations
function newRec(){

    $.ajax({
        url: "../rest_reclamations/",
        type: "GET",
        success: function (data) {
            new_r.textContent = data.length
            if (data.length == 0) {
                new_r.classList.remove("new-reclamation")
            } else {
                new_r.classList.add("new-reclamation")
            }

        },
        error: function (errors) {
            console.log(errors)
        }

    })
}


// get the number of noted reclamations

function notedRec(){
    $.ajax({
        url: "../rest_notes/",
        type: "GET",
        success: function (data) {
            noted_r.textContent = data.length
            if (data.length == 0) {
                noted_r.classList.remove("new-reclamation")
            } else {
                noted_r.classList.add("new-reclamation")
            }

        },
        error: function (errors) {
            console.log(errors)
        }

    })
}

setInterval(function () { notedRec(); }, 1000)
setInterval(function () { newRec(); }, 1000)