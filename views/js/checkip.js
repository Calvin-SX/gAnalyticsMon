function checkip(ipaddr) {
    var ipaddr = document.getElementById("checkip").value;
    var url = "/ipaddress/" + ipaddr;

    fetch(url).then((response) => response.json()).then((jsonData) =>{
        console.log(jsonData);
        if (jsonData['badip']){
            document.getElementById("ipreputation").innerHTML = "The IP address is BAD."
        }
        else {
            document.getElementById("ipreputation").innerHTML = "Nothing bad found for this IP address."
        }
    });
}