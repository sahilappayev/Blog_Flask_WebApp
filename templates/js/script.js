function setTitle(title){
    var spanTitle = document.getElementById("deleteTitle");
    console.log(" Span Title ",spanTitle);
    spanTitle.innerHTML = title;
}

function setId(id){
    var formDelete = document.getElementById('deleteId');
    console.log("Article id", id);
    formDelete.action = '/article/'+ id;
}