var ctx = document.getElementById('radar');

var features_var = document.getElementById("features_var").value;
features_var = features_var.replace('[','')
features_var = features_var.replace(']','')
features_var = features_var.replaceAll("'",'')
features_var = features_var.split(",");

var human_var = document.getElementById("human_data_var").value;
var human_var = human_var.replace('[','');
var human_var = human_var.replace(']','');
var human_var = human_var.split(","); 

var bot_var = document.getElementById("bot_data_var").value;
var bot_var = bot_var.replace('[','');
var bot_var = bot_var.replace(']','');
var bot_var = bot_var.split(",");


var config =  {
    type: 'radar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: 'Human',
            data: [12, 19, 3, 5, 2, 3],
            fill: true,
            backgroundColor: "rgba(179,181,198,0.2)",
            borderColor: "rgba(179,181,198,1)",
            pointBorderColor: "#fff",
            pointBackgroundColor: "rgba(179,181,198,1)",
            },   
            {
            label: 'bot',
            data: [31, 21, 6, 9, 10, 30],
            fill: true,
            backgroundColor: "rgba(255,99,132,0.2)",
            borderColor: "rgba(255,99,132,1)",
            pointBorderColor: "#fff",
            pointBackgroundColor: "rgba(255,99,132,1)",
            pointBorderColor: "#fff",
            }
        ]
        },
        options: {
            legend:{
                display: true,
                labels:{
                    // fontColor:"Red",
                    fontSize:20
                }
            },
            responsive: false,
            scales: {
                // xAxes:[{
                //     gridLines:{
                //         lineWidth:0
                //     }
                    
                // }],
                // yAxes: [{
                //     gridLines:{
                //         lineWidth:0
                //     },
                //     ticks: {
                //         beginAtZero: true
                //     }
                // }]
            },
        }
    };


     // 라벨 변경
     var labels = config.data.labels;
     console.log(labels);
     for(var i=0; i<labels.length; i++){
         labels[i] = features_var[i]
     }

     // human 데이터 변경
    var human_datasets = config.data.datasets[0].data;
    for(var i=0; i<human_datasets.length; i++){
        human_datasets[i] = human_var[i]
    }

    // bot 데이터 변경
    var bot_datasets = config.data.datasets[1].data;
    for(var i=0; i<bot_datasets.length; i++){
        bot_datasets[i] = bot_var[i]
    }

    var myChart = new Chart(ctx,config);