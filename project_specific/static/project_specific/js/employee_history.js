let transaction_history = JSON.parse(document.getElementById("transaction_history").textContent)
let order_history = JSON.parse(document.getElementById("order_history").textContent)

function drawTransactionHistory() {
    let data = []
    for (var i=0; i<transaction_history.length; i++) {
        transaction = transaction_history[i]
        data.push({x: new Date(transaction['timestamp']),
    y:transaction['balance_after']})
    }
    
    var chart = new Chartist.Line('.ct-chart', {
        series: [
          {
            name: 'series-1',
            data: data
          },
        ]
      }, {
        axisX: {
          type: Chartist.FixedScaleAxis,
          divisor: 5,
          labelInterpolationFnc: function(value) {
            return moment(value).format('MMM D');
          }
        }
      });
}

function downloadPastTransactionHistory() {
    let startDate = $("#startDate").val()
    let endDate = $("#endDate").val()
    if (startDate == "") {
        alert("Please enter start date to start download")
    } else {        
        if (endDate == "") {
            let ms = new Date(). getTime() + 86400000;
            endDate = parseDate(new Date(ms));
        }
        if (startDate > endDate) {
          // swap around if it is different
          let intermediate_start = startDate
          startDate = endDate
          endDate = intermediate_start
        }
        window.open(`/main/employee/export_transaction_history/${startDate}/${endDate}/`)
    }
}

if (transaction_history) {
  drawTransactionHistory();
}

// var data = {
// // A labels array that can contain any sort of values
// labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
// // Our series array that contains series objects or in this case series data arrays
// series: [
//     [5, 2, 4, 2, 0]
// ]
// };

// // Create a new line chart object where as first parameter we pass in a selector
// // that is resolving to our chart container element. The Second parameter
// // is the actual data object.
// new Chartist.Line('.ct-chart', data);

// Drawing a donut chart
// new Chartist.Pie('.ct-chart', {
//     series: [10, 2, 4, 3]
//   }, {
//     donut: true
//   });