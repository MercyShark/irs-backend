const fileDropArea = document.getElementById("fileDropArea");
const fileList = document.getElementById("fileList");
const fileInput = document.getElementById("fileInput");
const urlInput = document.getElementById("urlInput");
const siteList = document.getElementById("siteList");
const form = document.getElementById("form");
const hiddenInput = document.getElementById("hiddenInput");

let urls = [];

fileDropArea.addEventListener("dragover", (event) => {
  event.preventDefault();
  fileDropArea.classList.add("active");
});

fileDropArea.addEventListener("dragleave", () => {
  fileDropArea.classList.remove("active");
});

fileDropArea.addEventListener("drop", (event) => {
  event.preventDefault();
  fileDropArea.classList.remove("active");
  const files = event.dataTransfer.files;
  handleFiles(files);
});

document.getElementById("fileInput").addEventListener("change", (event) => {
  const files = event.target.files;
  if (files.length > 0) {
    // clearClient();
    document.getElementById("upload_button").disabled = false;
  }
  handleFiles(files);
});

function handleFiles(files) {
  //   for (const file of files) {
  //     const listItem = document.createElement('li');
  //     listItem.className = 'file-list-item';
  //     listItem.textContent = file.name;
  //     fileList.appendChild(listItem);
  //   }
  for (const file of files) {
    const listItem = document.createElement("li");
    listItem.className =
      "file-list-item d-flex justify-content-between my-2 p-2";
    const fileInfo = document.createElement("div");
    fileInfo.className = "d-flex";
    const fileType = getFileTypeIcon(file.type);
    fileInfo.innerHTML = `${fileType} <div class="file-info mx-3"><span>${
      file.name
    }</span><br><small class="file-details">  ${(file.size / 1024).toFixed(
      2
    )} KB</small></div>`;
    listItem.appendChild(fileInfo);
    const previewButton = document.createElement("img");
    previewButton.src = "../static/icons/tick.png";
    previewButton.className = "btn  btn-sm mt-3 mx-2";
    listItem.appendChild(previewButton);
    fileList.appendChild(listItem);
  }
}

function clearClient() {
  document.getElementById("upload_button").disabled = true;
  fileList.innerHTML = "";
  if (fileInput.value) {
    try {
      fileInput.value = ""; //for IE11, latest Chrome/Firefox/Opera...
    } catch (err) {}
    if (fileInput.value) {
      //for IE5 ~ IE10
      var form = document.createElement("form"),
        parentNode = f.parentNode,
        ref = fileInput.nextSibling;
      form.appendChild(fileInput);
      form.reset();
      parentNode.insertBefore(fileInput, ref);
    }
  }
}

function getFileTypeIcon(fileType) {
  if(fileType.endsWith("html")){
    return `<img src="../static/icons/html.png" alt="">`;
  }
  else if(fileType.endsWith("pdf")){
    return `<img src="../static/icons/pdf.png" alt="">`;
  }
  else if (fileType.startsWith("image/")) {
    return `<img src="../static/icons/image.png" alt="">`;
  } else if (fileType.startsWith("text/")) {
    return `<img class="img-fluid" src="../static/icons/text.png" alt="">`;
  } else {
    return `<img src="../static/icons/pdf.png" alt="">`;
  }
}


function addUrl() {
  let url = urlInput.value;
  urlInput.value = "";
  if (validateURL(url)) {
  urls.push(url);
  }
  showUrl();
  if(urls.length > 0) {
    document.getElementById("upload_button").disabled = false;
  }
}

function showUrl() {
  let child = siteList.lastElementChild;
  while (child) {
    siteList.removeChild(child);
    child = siteList.lastElementChild;
  }
  let count=0;
  for (let url of urls) {
    const listItem = document.createElement("li");
    listItem.className = "my-2 p-2";
    listItem.id = count;
    const sitelist = document.createElement("div");
    sitelist.className = "d-flex justify-content-between";
    sitelist.innerHTML = `<span>${url}</span><button type="button" class="btn-close" id=${count} aria-label="Close" onclick="clearUrl(this.id)"></button>`;
    listItem.appendChild(sitelist);

    siteList.appendChild(listItem);
    count++;
  }
}

function clearUrl(id){
  var elem = document.getElementById(id);
  console.log(id);
  elem.parentNode.removeChild(elem);
  urls.splice(id,1);
  if(urls.length == 0) {
    document.getElementById("upload_button").disabled = true;
  }
}

function validateURL(url) {
  const regex = /^(http|https):\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/\S*)?$/;
  return regex.test(url);
}

function upload(){
  let links = urls.toString();
  hiddenInput.value = links;
  form.submit();
}
