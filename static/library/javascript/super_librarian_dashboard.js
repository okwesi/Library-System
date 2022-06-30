const librariansBox = document.getElementById('users');
const booksBox = document.getElementById('books');
const requestsBox = document.getElementById('requests-box');
const schoolBox = document.getElementById('schools-box');
const spinnerbox = document.getElementById("spinner-box")
const booksSpinnerBox = document.getElementById("books-spinner")
const requestSpinnerBox = document.getElementById("request-spinner")
const schoolSpinnerBox = document.getElementById("school-spinner")

// for add librarian  
const formLibrary = document.getElementById("librarian-form")
const emailField = document.getElementById("id_email")
const phoneField = document.getElementById("id_phone")
const password1Field = document.getElementById("id_password1")
const password2Field = document.getElementById("id_password2")
const nameField = document.getElementById("id_full_name")
var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value



const alertBox = document.getElementById("alert")
const url = window.location.origin




// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie != '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// };
// var csrftoken = getCookie('csrftoken');
// function csrfSafeMethod(method) {
//     // these HTTP methods do not require CSRF protection
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }
// $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     }
// });


// this ajax call get librarians from the library of the super librarian
getLibrarians()

function getLibrarians() {
    $.ajax({
        type: 'GET',
        url: "library/query-librarians/",
        success: function (response) {
            console.log(response.data)

            spinnerbox.classList.add("not-visible")
            const data = response.data;

            data.forEach(element => {
                librariansBox.innerHTML += `
               <tr>
                    <td>${element.name}</td>
                    <td>${element.email}</td>
                    <td>${element.phone}</td>
                    <td>${element.last_login}</td>
                    <td>${element.group}</td>
                    <td><button type="button" class="btn btn-danger mb-2" >
                    <i style="font-size:large;" class="bi bi-trash-fill"></i>
                  </button>
                  </td>

                </tr>
            `
            });
        },
        error: function (error) {
            console.log("error", error)
        }

    })
}

formLibrary.addEventListener('submit', e => {
    e.preventDefault()
    $.ajax({
        type: 'POST',
        url: '/users/accounts/librarian-registration/',
        data: {
            csrfmiddlewaretoken: csrf_token,
            email: emailField.value,
            phone: phoneField.value,
            password1: password1Field.value,
            password2: password2Field.value,
            full_name: nameField.value
        },
        success: function (response) {
            console.log(response)
            librariansBox.innerHTML = ""
            getLibrarians()
            formLibrary.reset();
            $('#addLibrarianModal').modal('hide')
            handleAlert('success', "New librarian Added !!!")
            document.getElementById("librarian-form").reset()

        },
        error: function (error) {
            console.log('error', error)
            handleAlert('danger', "Oops, Something went wrong !!")
        }
    })
})





const form = document.getElementById("book-form")
const title = document.getElementById("id_title")
const about = document.getElementById("id_about")
const stock = document.getElementById("id_stock")

form.addEventListener('submit', e => {
    e.preventDefault()
    $.ajax({
        type: 'POST',
        url: '/books/add/',
        data: {
            csrfmiddlewaretoken: csrf_token,
            title: title.value,
            about: about.value,
            stock: stock.value,
        },
        success: function (response) {
            getBooks()

            form.reset();
            document.getElementById('alert').classList.add("alert-success");
            document.getElementById('alert').innerHTML = '<b>Book Added!!!</b>';
            setTimeout(function () {
                document.getElementById('alert').style.display = "none";
            }, 2000);
            $('#addBookModal').modal('hide')

        },
        error: function (error) {
            console.log('error', error)
            document.getElementById('alert').classList.add("alert-danger");
            document.getElementById('alert').innerHTML = error;
            setTimeout(function () {
                document.getElementById('alert').style.display = "none";
            }, 2000);
        }
    })
})


getBooks()

function getBooks() {
    $.ajax({
        type: 'GET',
        url: "/books/get-books/",
        success: function (response) {
            console.log(response.data)
            setTimeout(() => {
                booksSpinnerBox.classList.add("not-visible")
                const data = response.data;

                data.forEach(element => {
                    booksBox.innerHTML += `
                <div class="col-sm-6 col-lg-3 mb-4">
                    <div class="card text-right text-light bg-dark " style="width: 18rem;">
                    <div class="card-body">
                    <h5 class="card-title">${element.book_id}</h5>
                    <h5 class="card-title">${element.title}</h5>
                    <p class="card-text">${element.about}</p>
                    <p class="card-text">${element.stock}</p>                    
                    <p class="card-text">${element.library}</p>                    
                    <a href="${url}/books/${element.book_id}" class="btn btn-success"  id="update"><i style="font-size:large;" class="bi bi-pen-fill">Read More</i></a>
                    
                    </div>
                    </div>
                    </div>
                    `
                });
            }, 2000)
        },
        error: function (error) {
            console.log("error", error)
        }

    })
}



///////////////////////////// REQUEST ///////////////////////////////////

getRequests()

function getRequests() {
    $.ajax({
        type: 'GET',
        url: "/request/librarian_get_grouped_requests/",
        success: function (response) {
            console.log(response.data)

            setTimeout(() => {
                requestSpinnerBox.classList.add("not-visible")
                const data = response.data;

                data.forEach(element => {
                    requestsBox.innerHTML += `
                    <div class="col-sm-6 col-lg-3 mb-4">
                        <div class="card text-right text-light bg-dark " style="width: 18rem;">
                        <div class="card-body">
                        <h5 class="card-title">${element.id}</h5>
                        <h5 class="card-title">${element.school}</h5>
                        <p class="card-text">${element.status}</p>
                        <p class="card-text">${element.count}</p>
                                           
                        <a href="${url}/request/details/${element.school_id}" class="btn btn-success"  id="update"><i style="font-size:large;" class="bi bi-pen-fill">Read More</i></a>
                        
                        </div>
                        </div>
                        </div>
                        `
                });
            }, 1000)


        },
        error: function (error) {
            console.log("error", error)
        }

    })
}
function refresh() {
    requestsBox.innerHTML = ""
    requestSpinnerBox.classList.remove("not-visible")
    getRequests()
}



////////////////////////////// SCHOOLS ///////////////////////////////////////
getSchools()

function getSchools() {
    $.ajax({
        type: 'GET',
        url: "/library/get-schools/",
        success: function (response) {
            console.log(response.data)

            setTimeout(() => {
                schoolSpinnerBox.classList.add("not-visible")
                const data = response.data;

                data.forEach(element => {
                    schoolBox.innerHTML += `
                        <div class="col-sm-6 col-lg-3 mb-4">
                            <div class="card text-right text-light bg-dark " style="width: 18rem;">
                            <div class="card-body">
                            <h5 class="card-title">${element.id}</h5>
                            <h5 class="card-title">${element.school_name}</h5>
                                                                           
                            </div>
                            </div>
                            </div>
                            `
                });
            }, 1000)
        },
        error: function (error) {
            console.log("error", error)
        }

    })
}
const formSchool = document.getElementById("school-form")
const schoolEmailField = document.getElementById("school_email")
const schoolPhoneField = document.getElementById("school_phone")
const schoolPassword1Field = document.getElementById("school_password1")
const schoolPassword2Field = document.getElementById("school_password2")
const schoolNameField = document.getElementById("school_name")
const schoolLocationField = document.getElementById("school_locations")
const schoolDigitalAddressField = document.getElementById("school_gps_location")

formSchool.addEventListener('submit', e => {
    e.preventDefault()
    $.ajax({
        type: 'POST',
        url: '/users/accounts/school-registration/',
        data: {
            csrfmiddlewaretoken: csrf_token,
            email: schoolEmailField.value,
            phone: schoolPhoneField.value,
            password1: schoolPassword1Field.value,
            password2: schoolPassword2Field.value,
            name: schoolNameField.value,
            locations: schoolLocationField.value,
            gps_location: schoolDigitalAddressField.value
        },  
        success: function (response) {
            console.log(response)
            schoolBox.innerHTML = ""
            getSchools()
            formLibrary.reset();
            $('#addSchoolModal').modal('hide')
            document.getElementById('alert').classList.add("alert-success");
            document.getElementById('alert').innerHTML = '<b>School Added!!!😊</b>';
            setTimeout(function () {
                document.getElementById('alert').style.display = "none";
            }, 3000);            formSchool.reset()

        },
        error: function (error) {
            console.log('error', error)
            document.getElementById('alert').classList.add("alert-success");
            document.getElementById('alert').innerHTML = '<b>Something Went Wrong!!!</b>';
            setTimeout(function () {
                document.getElementById('alert').style.display = "none";
            }, 2000);         }
    })
})