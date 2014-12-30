function showLabs(str) 
{alert("dfd")
    if (str == "")
    {
        document.getElementById("labs").innerHTML = "";
        return;
    } 
    else 
    {
        if (window.XMLHttpRequest) {
            // code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp = new XMLHttpRequest();
        } else {
            // code for IE6, IE5
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                document.getElementById("labs").innerHTML = xmlhttp.responseText;
            }
        }
        xmlhttp.open("GET","getlabs.php",true);
        xmlhttp.send();
    }
}

function hello(){
	
  var op0 = document.getElementById("None").value;
  var op1 = document.getElementById("status").value;
  var op2 = document.getElementById("int_level").value;
  var op3 = document.getElementById("source_avail").value;
    if (op1){
    	alert("skssax")
    	add_status(op1);
       }
  	else if (op2){
  		add_inte(op2);
  	}
  	else if (op3) 
  		{
  			add_source(op3);
  		}
  	else alert("none")
 }
function add_status(op1)
 {
 	alert("inside add_status")
 	document.getElementById('status_id').className = "new_stt";
 	return();
}
function add_inte(op2){
	 	document.getElementById('integration_level_id').className = "new_stt";
}
function add_source(op3)
 {
 	document.getElementById('source_avail_id').className = "new_stt";
 	
}
