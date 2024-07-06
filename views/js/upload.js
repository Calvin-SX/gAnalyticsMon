function upload(file) {
    const filename = document.getElementById("input-file").value;
    var res = new Response(file);
    res.text().then(text => {
        console.log(text);
    })
    console.log("upload file: " + filename);
}