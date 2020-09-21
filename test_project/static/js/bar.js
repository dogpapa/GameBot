var ctx = document.getElementById('bar');
console.log("들어왔나요?")
var bar_features_var = document.getElementById("bar_features_var").value;
bar_features_var = bar_features_var.replace('[','')
bar_features_var = bar_features_var.replace(']','')
bar_features_var = bar_features_var.replaceAll("'",'')
bar_features_var = bar_features_var.split(",");

var bar_data_var = document.getElementById("bar_data_var").value;
bar_data_var = bar_data_var.replace('[','');
bar_data_var = bar_data_var.replace(']','');
bar_data_var = bar_data_var.split(","); 

var config = {
    type: 'horizontalBar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],  
        datasets: [{
            label: 'Weight',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                // 'rgba(54, 162, 235, 0.2)',
                    // 'rgba(179,181,198,0.2)'
                "#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#666666"
                ],
            borderColor: [
                // 'rgba(54, 162, 235, 1)',
                    'rgba(179,181,198,0.2)'
                ],
            borderWidth: 1
            },
            // {
            // label: 'bot',
            // data: [31, 21, 6, 9, 10, 30],
            // backgroundColor: [
            //     // 'rgba(255, 99, 132, 0.2)',
            //     // 'rgba(54, 162, 235, 0.2)',
            //     // 'rgba(255, 206, 86, 0.2)',
            //     // 'rgba(75, 192, 192, 0.2)',
            //     // 'rgba(153, 102, 255, 0.2)',
            //     // 'rgba(255, 159, 64, 0.2)'
            //     'rgba(255, 99, 132, 0.2)',
            //     'rgba(255, 99, 132, 0.2)',
            //     'rgba(255, 99, 132, 0.2)',
            //     'rgba(255, 99, 132, 0.2)',
            //     'rgba(255, 99, 132, 0.2)',
            //     'rgba(255, 99, 132, 0.2)'
            //     ],
            // borderColor: [
            //     // 'rgba(255, 99, 132, 1)',
            //     // 'rgba(54, 162, 235, 1)',
            //     // 'rgba(255, 206, 86, 1)',
            //     // 'rgba(75, 192, 192, 1)',
            //     // 'rgba(153, 102, 255, 1)',
            //     // 'rgba(255, 159, 64, 1)'
            //     'rgba(255, 99, 132, 1)',
            //     'rgba(255, 99, 132, 1)',
            //     'rgba(255, 99, 132, 1)',
            //     'rgba(255, 99, 132, 1)',
            //     'rgba(255, 99, 132, 1)',
            //     'rgba(255, 99, 132, 1)'
            //     ],
            // borderWidth: 1
            // }
            
        ]
        },
        options: {
            legend:{
                display: false,
                labels:{
                    fontSize:20
                }
            },
            responsive: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        // mirror: true
                    }
                }]
            },
        }
    };

    // 라벨 변경
    var labels = config.data.labels;
    console.log(labels);
    for(var i=0; i<labels.length; i++){
        labels[i] = bar_features_var[i]
    }
    // human 데이터 변경
    var bar_datasets = config.data.datasets[0].data;
    for(var i=0; i<bar_datasets.length; i++){
        bar_datasets[i] = bar_data_var[i]
    }

    // bot 데이터 변경
    // var bot_datasets = config.data.datasets[1].data;
    // for(var i=0; i<bot_datasets.length; i++){
    //     bot_datasets[i] = bot_var[i]
    // }


    var myChart = new Chart(ctx, config);

    // //데이터 변경
	// document.getElementById('reData').onclick = function(){
		
	// 	//데이터셋 수 만큼 반복
	// 	var dataset = config.data.datasets;
	// 	for(var i=0; i<dataset.length; i++){
	// 		console.log(dataset);
	// 		//데이터 갯수 만큼 반복
	// 		var data = dataset[i].data;
	// 		for(var j=0 ; j < data.length ; j++){
	// 			data[j] = Math.floor(Math.random() * 50);
	// 		}
	// 	}
		
	// 	myChart.update();	//차트 업데이트
	// }
	
	// //데이터 추가
	// document.getElementById('addData').onclick = function(){
		
	// 	//라벨추가
	// 	config.data.labels.push('data'+config.data.labels.length)
		
	// 	//데이터셋 수 만큼 반복
	// 	var dataset = config.data.datasets;
	// 	for(var i=0; i<dataset.length; i++){
	// 		//데이터셋의 데이터 추가
	// 		dataset[i].data.push(Math.floor(Math.random() * 50));
	// 	}
	// 	myChart.update();	//차트 업데이트
	// }
	
	// //데이터셋 추가
	// document.getElementById('addDataSet').onclick = function(){
	// 	var color1 = Math.floor(Math.random() * 256);
	// 	var color2 = Math.floor(Math.random() * 256);
	// 	var color3 = Math.floor(Math.random() * 256);
		
	// 	console.log(color1 + " " + color2 + " " + color3)
		
	// 	var newDataset = {
	// 		label: 'new Dataset'+config.data.datasets.length,
	// 		borderColor : 'rgba('+color1+', '+color2+', '+color3+', 1)',
	// 		backgroundColor : 'rgba('+color1+', '+color2+', '+color3+', 1)',
	// 		data: [],
	// 		fill: false
	// 	}
		
	// 	// newDataset에 데이터 삽입
	// 	for (var i=0; i< config.data.labels.length; i++){
	// 		var num = Math.floor(Math.random() * 50);
	// 		newDataset.data.push(num);
	// 	}
		
	// 	// chart에 newDataset 푸쉬
	// 	config.data.datasets.push(newDataset);
		
	// 	myChart.update();	//차트 업데이트
	// }
	
	// //데이터 삭제
	// document.getElementById('delData').onclick = function(){
		
	// 	config.data.labels.splice(-1,1);//라벨 삭제
		
	// 	//데이터 삭제
	// 	config.data.datasets.forEach(function(dataset) {
	// 		dataset.data.pop();
	// 	});
		
	// 	myChart.update();	//차트 업데이트
	// }
	
	// //데이터셋 삭제
	// document.getElementById('delDataset').onclick = function(){
	// 	config.data.datasets.splice(-1,1);
	// 	myChart.update();	//차트 업데이트
	// }