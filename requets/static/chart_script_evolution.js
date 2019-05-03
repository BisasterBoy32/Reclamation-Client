$(document).ready(function(){
  var data_url = "/manager/chart_data/"
  var weeks = []
  var reclamation = []
  $.ajax({
    method : "GET",
    url : data_url,
    success : function(data){
      weeks = data.weeks
      reclamation = data.reclamation_week
      my_chart()
    },
    error : function(errors){
      console.log("error happened: ")
      console.log(errors)
    }
  })

  function my_chart(){
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: weeks,
                datasets: [{
                    label: 'Reclamation ',
                    data: reclamation,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
  }
})
