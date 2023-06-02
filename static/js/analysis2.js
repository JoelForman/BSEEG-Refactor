console.log("Successfully passed final_avg1...");
console.log(final_avg1);
console.log("SUccessfully passed final_avg2...");
console.log(final_avg2);

final_avg1 = final_avg1.map(function (value) {
  return value === 0 ? null : value;
});

final_avg2 = final_avg2.map(function (value) {
  return value === 0 ? null : value;
});

// old dummy data: [2,2.5,2.6,1.9,2.7,2.3,3.1,3.5,3.3,3.5,3.9,4.3,3.9,3.4,3.0,2.3,3.1,3.5,3.3,3.5,3.9,2.3,3.1,3.5,3.3,]
// old dummy data 2: data: [2.5,3.3,3.5,3.9,2.3,2,2.5,3.9,3.4,3.0,2.3,3.1,3.5,3.1,3.5,3.3,3.5,3.9,4.3,3.3,3.5,3.9,2.3,3.1,3.5,3.3,]

let time = Array.from({ length: final_avg1.length }, (_, i) => i);

new Chart(document.getElementById("line-chart"), {
  type: "line",
  data: {
    labels: time,
    datasets: [
      {
        data: final_avg1,
        label: "EEG1",
        borderColor: "#3e95cd",
        fill: false,
      },
      {
        data: final_avg2,
        label: "EEG2",
        borderColor: "#8e5ea2",
        fill: false,
      },
    ],
  },
  options: {
    title: {
      display: true,
      text: "BSEEG Scores",
    },
    scales: {
      yAxes: [
        {
          scaleLabel: {
            display: true,
            labelString: "probability",
          },
        },
      ],
    },
  },
});

function convertToCSV(data) {
  var csv = "Hour,EEG1,EEG2\n";
  data.forEach(function (row) {
    csv += row.join(",") + "\n";
  });
  return csv;
}

function downloadCSV(filename, csvData) {
  var csvFile = new Blob([csvData], { type: "text/csv" });

  // Check if the browser supports the download attribute
  if (window.navigator && window.navigator.msSaveOrOpenBlob) {
    // For IE browser
    window.navigator.msSaveOrOpenBlob(csvFile, filename);
  } else {
    // For other browsers
    var downloadLink = document.createElement("a");
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.download = filename;

    // Append the link to the DOM
    document.body.appendChild(downloadLink);

    // Simulate a click event to trigger the download
    downloadLink.click();

    // Clean up
    document.body.removeChild(downloadLink);
  }
}

function saveCSV() {
  // Combine scores and times into a 2D array
  var data = [];
  for (var i = 0; i < final_avg1.length; i++) {
    data.push([time[i], final_avg1[i], final_avg2[i]]);
  }

  // Convert the data to CSV format
  var csvData = convertToCSV(data);

  // Provide a filename for the CSV file
  var filename = "data.csv";

  // Call the downloadCSV function
  downloadCSV(filename, csvData);
}

// Attach the saveCSV function to the button click event
var saveButton = document.getElementById("saveButton");
saveButton.addEventListener("click", saveCSV);
