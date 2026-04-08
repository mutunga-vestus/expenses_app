const renderChart = (data, labels) => {
  const ctx = document.getElementById("myChart").getContext("2d");

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [{
        label: "Last 6 months expenses",
        data: data,
        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
          "rgba(75, 192, 192, 0.6)",
          "rgba(153, 102, 255, 0.6)",
          "rgba(255, 159, 64, 0.6)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
        ],
        borderWidth: 1,
      }],
    },
    options: {
  plugins: {
    title: {
      display: true,
      text: "Income per Source",
    },
    legend: {
      position: "top",
    }
  }
}
  });
};

const getChartData = () => {
  console.log("fetching");

  fetch("/income/income_summary/")
    .then(res => res.json())
    .then(results => {
      console.log("results", results);

      const category_data = results.income_data;
      const labels = Object.keys(category_data);
      const data = Object.values(category_data);

      renderChart(data, labels);
    })
    .catch(err => console.error(err));
};

document.addEventListener("DOMContentLoaded", getChartData);
