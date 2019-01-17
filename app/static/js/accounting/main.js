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


function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}

window.onload = function() {

	var data = tags['result'];

	var names = [];
	var costs = [];
	var colors = [];

	var dynamicColors = function() {
            var r = Math.floor(Math.random() * 255);
            var g = Math.floor(Math.random() * 255);
            var b = Math.floor(Math.random() * 255);
            return "rgb(" + r + "," + g + "," + b + ")";
         };

	for (var i = 0; i < data.length; i++) {
		names.push(data[i]['name']);
		costs.push(parseFloat(data[i]['cost']).toFixed(2));
		colors.push(dynamicColors())
	}

	var config = {
			type: 'pie',
			data: {
				datasets: [{
					data: costs,
					backgroundColor: colors
				}],
				labels: names
			},
			options: {
				responsive: true
			}
		};
	var ctx = document.getElementById('chart-area').getContext('2d');
	window.myPie = new Chart(ctx, config);
};
