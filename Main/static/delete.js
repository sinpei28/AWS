deleteBtn = document.getElementById("deleteBtn");
cancelDeleteBtn = document.getElementById("cancelDeleteBtn");
empID = document.getElementById("emp-id").innerHTML

deleteBtn.addEventListener("click", () =>{
    console.log(empID)
})

cancelDeleteBtn.addEventListener("click", () =>{
    window.location = "/deleteEmployee"
})