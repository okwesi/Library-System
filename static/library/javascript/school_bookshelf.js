const booksBox = document.getElementById('student-books');
const booksSpinnerBox = document.getElementById("books-spinner")
const loadBtn = document.getElementById("load-btn")
const endbox = document.getElementById('end-box')
const url = window.location.origin
let num_books = 3
getBooks()

function getBooks() {
    $.ajax({
        type: 'GET',
        url: `/user/school/get_books/${num_books}/`,
        success: function (response) {
            console.log(response.data)
            setTimeout(() => {
                booksSpinnerBox.style.display = "none";
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
                    
                    <a href="${url}/user/school/${element.book_id}" class="btn btn-success"  id="update"><i style="font-size:large;" class="bi bi-pen-fill">Read More</i></a>
                    </div>
                    </div>
                    </div>
                    `
                });
            }, 100)
        },
        error: function (error) {
            console.log("error", error)
        }

    })
}


loadBtn.addEventListener('click', () => {
    booksSpinnerBox.style.display = "block";
    num_books += 3
    getBooks()
})


const alertShelf = document.getElementById("alert")
if (alertShelf){
    document.getElementById('alert').classList.add("alert-success"); 
    // document.getElementById('alert').innerHTML='<b>Book Added!!!</b>'; 
            setTimeout(function() {
                document.getElementById('alert').style.display = "none";
                 },2000);
}




// BOOK SHELF DETAILS SCRIPTS HERE
