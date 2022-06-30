const backBtn = document.getElementById("back-btn")

backBtn.addEventListener('click', ()=>{
    history.back()
    document.getElementById('nav-home').classList.remove("active")
    document.getElementById('nav-profile').classList.add("active")
})




