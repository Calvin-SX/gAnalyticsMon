const pieXValues = [];
const pieYValues = [];
const barColors = [
  "#b91d47",
  "#00aba9",
  "#2b5797",
  "#e8c3b9",
  "#1e7145"
];
readDaily();

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