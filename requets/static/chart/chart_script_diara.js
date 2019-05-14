$(document).ready(function(){
  var data_url = "/manager/chart_data/"
  var daira = []
  var reclamation = []
  $.ajax({
    method : "GET",
    url : data_url,
    success : function(data){
      daira = data.daira
      reclamation = data.reclamations
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
            type: 'pie',
            data: {
                labels: daira,
                datasets: [{
                    label: 'Reclamation ',
                    data: reclamation,
                    backgroundColor: [
                        'rgb(0, 255, 255)',
                        'rgb(204, 102, 255)',
                        'rgb(255, 80, 80)',
                        'rgb(255, 204, 0)',
                        'rgb(102, 153, 0)',
                        'rgb(0, 51, 0)'
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
