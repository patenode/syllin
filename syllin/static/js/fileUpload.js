(function() {
  document.getElementById("fileupload").onchange = function(){
    var files = document.getElementById("fileupload").files;
    var file = files[0];
    if(!file){
      return alert("No file selected.");
    }
    document.getElementById("spinner").removeAttribute("hidden");
    getSignedRequest(file);
  };
})();

function getSignedRequest(file){
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
  xhr.onreadystatechange = function(){
    if(xhr.readyState === 4){
      if(xhr.status === 200){
        var response = JSON.parse(xhr.responseText);
        uploadFile(file, response.data, response.url);
      }
      else{
        alert("Could not get signed URL.");
        document.getElementById("spinner").setAttribute("hidden", true);

      }
    }
  };
  xhr.send();
}

function uploadFile(file, s3Data, url){
  var xhr = new XMLHttpRequest();
  xhr.open("POST", s3Data.url);

  var postData = new FormData();
  for(key in s3Data.fields){
    postData.append(key, s3Data.fields[key]);
  }
  postData.append('file', file);

  xhr.onreadystatechange = function() {
    if(xhr.readyState === 4){
      if(xhr.status === 200 || xhr.status === 204){
        if (document.getElementById("s3_data_url")){
          document.getElementById("s3_data_url").value = url;
        }
        if (document.getElementById("preview")){
          document.getElementById("preview").src = url;
        }
        document.getElementById("submit").removeAttribute("disabled");
      }
      else{
        alert("Could not upload file.");
      }
   }
   document.getElementById("spinner").setAttribute("hidden", true);
  };
  xhr.send(postData);
}