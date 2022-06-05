	//Validtion Code For Inputs

var road = document.forms['form']['road'];


var road_error = document.getElementById('road_error');


road.addEventListener('textInput', road_Verify);


function validated(){
	if (road.value == "None") {
		road.style.border = "1px solid red";
		road_error.style.display = "block";
		road.focus();
		return false;
	}

}
function road_Verify(){
	if (road.value != "None"){
		return true;
	}
	
}