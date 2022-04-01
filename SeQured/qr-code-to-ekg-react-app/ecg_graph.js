//install plotly.js

//example array
var array = [3,3,3,3,3,3,3.5,4,4.3,3,-1,10,3,2,5,6,3,3,3,3,3,3];

var xValues = [];

for (var x = 0; x <= array.length; x += 1) {
  xValues.push(x);
}

var data = [{x:xValues, y:array, mode:"scatter"}];
var layout = {title: "ECG"};

Plotly.newPlot('myDiv', data, layout, {scrollZoom: true});
