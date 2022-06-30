const booksBox = document.getElementById('books');
const booksSpinnerBox = document.getElementById("books-spinner")

const alertBox = document.getElementById("alert")
const url = window.location.origin 



function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
// this ajax call get librarians from the library of the super librarian




const form = document.getElementById("book-form")
const title = document.getElementById("id_title")
const about = document.getElementById("id_about")
const stock = document.getElementById("id_stock")
var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value

form.addEventListener('submit', e => {
    e.preventDefault()
    $.ajax({
        type: 'POST',
        url : '/books/add/',
        data : {
            csrfmiddlewaretoken :  csrf_token,
            title : title.value,
            about : about.value,
            stock : stock.value,
        },
        success: function(response){
            console.log(response.data)
            getBooks()
            form.reset();
            document.getElementById('alert').classList.add("alert-success"); 
            document.getElementById('alert').innerHTML='<b>Book Added!!!</b>'; 
            setTimeout(function() {
                document.getElementById('alert').style.display = "none";
                 },2000);
            $('#addBookModal').modal('hide')
        },
        error: function(error){
            console.log('error', error )
        }
    })
})

getBooks()
function getBooks(){
$.ajax({
    type: 'GET',
    url: "/books/get-books/",
    success: function (response) {
        console.log( response.data)

        // booksSpinnerBox.classList.add("not-visible")
        booksSpinnerBox.style.display = 'none';
        const data = response.data;

        data.forEach(element => {
            booksBox.innerHTML += `
                <div class="col-sm-6 col-lg-3 mb-4">
                    <div class="card text-right text-light bg-dark " style="width: 18rem;">
                    <div class="card-body">
                    <h5 class="card-title">${element.title}</h5>
                    <p class="card-text">${element.about}</p>
                    <p class="card-text">${element.stock}</p>                    
                    <p class="card-text">${element.library}</p>                    
                    <a href="${url}/books/${element.book_id}" class="btn btn-success"><i style="font-size:large;" class="bi bi-pen-fill"></i>Read More</a>
                    </div>
                    </div>
                </div>
            `
        });
    },
    error: function (error) {
        console.log("error", error)
    }

})
}
       


$.ajax({
    type: 'GET',
    url: "request/librarian_get_student_request/",
    success: function (response) {
        console.log( response.data)

        booksSpinnerBox.classList.add("not-visible")
        const data = response.data;

        
    },
    error: function (error) {
        console.log("error", error)
    }

})





















