function calculate_cost_by_tag(e) {
	tag_id = e.childNodes[1].value
	tag_name = e.childNodes[3].value

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
	    	document.getElementById("cost_by_tag").innerHTML = 'cost by : ' + tag_name + ', $' + parseFloat(this.responseText).toFixed(2);
	  	}
	};
	xhttp.open("GET", "cost_by_tag/" + tag_id, true);
	xhttp.send();
}