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

function sort_current_tag_list_by_similarity(e) {
    var data = tags['result'];

    for (var i = 0; i < data.length; i++) {
        data[i]['similarity'] = similarity(e.value, data[i]['name']);
    }
    data.sort(function(a, b) {
        return b['similarity']- a['similarity'];
    });

    var tags_drop_down_list = document.getElementById("account_tag_drop_down");

    tags_drop_down_list.options.length = 0;

    for (var i=0; i<data.length; i++){
        var option = document.createElement("option");
        option.text = data[i]['name'];
        option.value = data[i]['id'];
        tags_drop_down_list.appendChild(option);
    }
    tags_drop_down_list.options[0].selected = true;
}

function similarity(s1, s2) {
  var longer = s1;
  var shorter = s2;
  if (s1.length < s2.length) {
    longer = s2;
    shorter = s1;
  }
  var longerLength = longer.length;
  if (longerLength == 0) {
    return 1.0;
  }
  return (longerLength - editDistance(longer, shorter)) / parseFloat(longerLength);
}

function editDistance(s1, s2) {
  s1 = s1.toLowerCase();
  s2 = s2.toLowerCase();

  var costs = new Array();
  for (var i = 0; i <= s1.length; i++) {
    var lastValue = i;
    for (var j = 0; j <= s2.length; j++) {
      if (i == 0)
        costs[j] = j;
      else {
        if (j > 0) {
          var newValue = costs[j - 1];
          if (s1.charAt(i - 1) != s2.charAt(j - 1))
            newValue = Math.min(Math.min(newValue, lastValue),
              costs[j]) + 1;
          costs[j - 1] = lastValue;
          lastValue = newValue;
        }
      }
    }
    if (i > 0)
      costs[s2.length] = lastValue;
  }
  return costs[s2.length];
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
