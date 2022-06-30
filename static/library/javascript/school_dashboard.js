const studentRow = document.getElementById("student")
const booksRow = document.getElementById("books-row")
const spinnerBox = document.getElementById("student-table-spinner")
const booksBox = document.getElementById("books-table-spinner")
const schoolBookBox = document.getElementById("school-books-row")

 
$.ajax({
    type: 'GET',
    url: "/user/get_students/",
    success: function (response) {
        console.log( response.data)

        spinnerBox.style.display = "none";
        const data = response.data;

        data.forEach(element => {
            studentRow.innerHTML += `
               <tr>
               
                    <td>${element.name}</td>
                    <td>${element.email}</td>
                    <td>${element.phone}</td>
                    <td>${element.school_class}</td>
                    <td>${element.gender}</td>
                    <td>${element.address}</td>
                </tr>
            `
        });
    },
    error: function (error) {
        console.log("error", error)
    }

})




$.ajax({
   type: 'GET',
   url: "/request/approved/",
   success: function (response) {
       console.log( response.data)

       booksBox.style.display = "none";
       const data = response.data;

       data.forEach(element => {
        booksRow.innerHTML += `
              <tr>
                   <td>${element.id}</td>
                   <td>${element.book}</td>
                   <td>${element.student}</td>
                   <td>${element.student_class}</td>
                   <td>${element.status}</td>
                   
                   </tr>
           `
       });
   },
   error: function (error) {
       console.log("error", error)
   }
})






$.ajax({
   type: 'GET',
   url: "/request/school-request/requests",
   success: function (response) {
        console.log( response.data)
        data = response.data;
        data.forEach(element => {
        schoolBookBox.innerHTML += `
                <tr>
                   <td>${element.id}</td>
                   <td>${element.book}</td>
                   <td>${element.status}</td>                   
                   <td>${element.quantity}</td>                   
                </tr>
           `
       });       
       
   },
   error: function (error) {
       console.log("error", error)
   }
})

{/* <button onclick="myfunctionName('${element.id}')">Click</button> */}









function myfunctionName(String){
console.log(String)
}




