deleteBtn = document.getElementById("deleteBtn");
cancelDeleteBtn = document.getElementById("cancelDeleteBtn");
empID = document.getElementById("emp-id").innerHTML

deleteBtn.addEventListener("click", () =>{
    window.location = "/deleteEmployeeInfo/" + empID
})

cancelDeleteBtn.addEventListener("click", () =>{
    window.location = "/deleteEmployee"
})