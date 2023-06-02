function showFileName(input) {
  var fileName = input.files[0].name;
  document.getElementById("filename").innerHTML = fileName;
}

// var fileInput = document.getElementById("file-input");

// var dropArea = document.getElementById("drag-image");

// button.onclick = ()=>{
//     input.click();
// }

// fileInput.addEventListener("change", function(){
//     file = this.files[0];
//     dropArea.classList.add("active");
//     viewfile();
// });

// dropArea.addEventListener("dragover", (event)=>{
//     event.preventDefault();
//     dropArea.classList.add("active");
//     dragText.textContent = "Release to Upload File";
// });

// dropArea.addEventListener("dragleave", ()=>{
//     dropArea.classList.remove("active");
//     dragText.textContent = "Drag & Drop EDF File Here";
// });

// dropArea.addEventListener("drop", (event)=>{

//     console.log('dropped......');
//     event.preventDefault();
//     dragText.textContent = "File Uploaded Successfully";
//     orText.textContent = "";

//     fileInput.files = event.dataTransfer.files[0];
//     viewfile(fileInput);
// });

// function viewfile(input){
//     var fileName = input.files[0].name;
//     document.getElementById("filename").innerHTML = fileName;
// let fileType = file.type;
// let validExtensions = ["image/jpeg", "image/jpg", "image/png"];
// if(validExtensions.includes(fileType)){
//     let fileReader = new FileReader();
//     fileReader.onload = ()=>{
//     let fileURL = fileReader.result;
//     let imgTag = `<img src="${fileURL}" alt="image">`;
//     dropArea.innerHTML = imgTag;
//     }
//     fileReader.readAsDataURL(file);
// }else{
//     alert("This is not an Image File!");
//     dropArea.classList.remove("active");
//     dragText.textContent = "Drag & Drop to Upload File";
// }
// }
