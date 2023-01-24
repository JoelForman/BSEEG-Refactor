new Chart(document.getElementById("line-chart"), { 
    type: 'line',
    data: {
      labels: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15.,16,17,18,19,20,21,22,23,24],
      datasets: [{ 
          data: [2,2.5,2.6,1.9,2.7,2.3,3.1,3.5,3.3,3.5,3.9,4.3,3.9,3.4,3.0,2.3,3.1,3.5,3.3,3.5,3.9,2.3,3.1,3.5,3.3,],
          label: "EEG1",
          borderColor: "#3e95cd",
          fill: false
        }, { 
          data: [2.5,3.3,3.5,3.9,2.3,2,2.5,3.9,3.4,3.0,2.3,3.1,3.5,3.1,3.5,3.3,3.5,3.9,4.3,3.3,3.5,3.9,2.3,3.1,3.5,3.3,],
          label: "EEG2",
          borderColor: "#8e5ea2",
          fill: false
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'BSEEG Scores'
      },
      scales: {
      yAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'probability'
        }
      }]
    }
    }
  });