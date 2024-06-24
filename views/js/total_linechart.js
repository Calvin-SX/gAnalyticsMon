var xValues = [];
var yValues = [];
readDailySum();
// Note the <canvas with id =myChart must be added in front of the <script for this file
var linechart = new Chart("myChart", {
    type: "line",
    data: {
      labels: xValues,
      datasets: [{
        fill: false,
        lineTension: 0,
        backgroundColor: "rgba(0,0,255,1.0)",
        borderColor: "rgba(0,0,255,0.1)",
        data: yValues
      }]
    },
    options: {
      legend: {display: false},
      scales: {
        yAxes: [{ticks: {min: 6, max:16}}],
      }
    }
  });

  function readDailySum() {
    const url = "/dailysum";
    fetch(url).then((response) => response.json()).then((jsonData) => {
        dailysum = jsonData['dailysum'];
        xValues = [];
        yValues = [];

        var min = 100000;
        var max = 0;
        for (var i = 0; i < dailysum.length; i++) {
            daily = dailysum[i];
            linechart.data.labels.push(daily[0]);
            if (min > daily[1]) {
                min = daily[1];
            }
            if (max < daily[1]){
                max = daily[1];
            }
            linechart.data.datasets.forEach((dataset) => {
                dataset.data.push(daily[1]);
            })
        }
        linechart.options.scales = {
            legend: {display: false},
            scales: {
              yAxes: [{ticks: {min: min, max:max}}],
            }
          }

        linechart.update();
        readDaily();
    });
  }

const pieXValues = [];
const pieYValues = [];
const barColors = [
  "#b91d47",
  "#00aba9",
  "#2b5797",
  "#e8c3b9",
  "#1e7145"
];

var pieChart = new Chart("pieChart", {
  type: "pie",
  data: {
    labels: pieXValues,
    datasets: [{
      backgroundColor: barColors,
      data: pieYValues
    }]
  },
  options: {
    title: {
      display: true,
      text: "Users by cities"
    }
  }
});

function readDaily() {
    const url = "/daily";
    fetch(url).then((response) => response.json()).then((jsonData) =>{
        countries = jsonData;
        for (var i = 0; i < countries.length; i++) {
            country = countries[i];
            pieChart.data.labels.push(country[2]);
            pieChart.data.datasets.forEach((dataset) =>{
                dataset.data.push(country[1]);
            });
        }
        pieChart.options = {
            title: {
              display: true,
              text: "Users by cities"
            }
          }
        pieChart.update();
    });
}