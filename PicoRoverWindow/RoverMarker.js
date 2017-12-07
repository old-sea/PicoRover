///for MQTT
const topic_base="";

var clientId = "jsmqtt_" + (Math.floor(Math.random() * 100000));
var client = new Paho.MQTT.Client("localhost",9090,clientId );

//for window
var w1;
var w2;
var w3;

function onConnect(){
	//only subscribe topic
	client.subscribe("PicoRover/#")
}

function onConnectionLost(responseObject){
	if (responseObject.errorCode !== 0) {
		console.log("onConnectionLost:"+responseObject.errorMessage);

	}
}

function onMessageArrived(message){
	/*if(message.destinationName.match(/1st/)){
		console.log("a");
		if(message.payloadString.match(/A/)){
			var S1 = document.getElementById('1st-S');
			S1.innerHTML = message.payloadString;
		}
	}else if(message.destinationName.match(/2nd/)){
		console.log("b");
		if(message.payloadString.match(/A/)){
			var S2 = document.getElementById('2nd-S');
			S2.innerHTML = message.payloadString;
		}
	}else if(message.destinationName.match(/3rd/)){
		console.log("c");
		if(message.payloadString.match(/A/)){
			var S3 = document.getElementById('3rd-S');
			S3.innerHTML = message.payloadString;
		}
	}*/
	
	if(message.payloadString.match(/A/)){
		if(message.destinationName.match(/1st/)){
			console.log("Sa");
			var S1 = document.getElementById('1st-S');
			S1.innerHTML = message.payloadString;
		}else if(message.destinationName.match(/2nd/)){
			console.log("Sb");
			var S2 = document.getElementById('2nd-S');
			S2.innerHTML = message.payloadString;
		}else if(message.destinationName.match(/3rd/)){
			console.log("Sc");
			var S3 = document.getElementById('3rd-S');
			S3.innerHTML = message.payloadString;
		}
	}
	if(message.destinationName.match(/throughput/)){
		console.log("thoroughput")
		if(message.destinationName.match(/1st/)){
			console.log("Ta");
			var T1 = document.getElementById('1st-T');
			T1.innerHTML = message.payloadString.slice(0, 4) + "[Mbps]" ;
		}else if(message.destinationName.match(/2nd/)){
			console.log("b");
			var T2 = document.getElementById('2nd-T');
			T2.innerHTML = message.payloadString.slice(0, 4) + "[Mbps]";
		}else if(message.destinationName.match(/3rd/)){
			console.log("b");
			var T3 = document.getElementById('3rd-T');
			T3.innerHTML = message.payloadString.slice(0, 4) + "[Mbps]";
		}
	}
	console.log("onMsgRecv: " + message.payloadString + " DestName=" + message.destinationName);
	if(message.payloadString.match(/1st/)){
		drawMark(0,"nom");
	}else if(message.payloadString.match(/2nd/)){
		drawMark(1,"nom");
	}else if(message.payloadString.match(/3rd/)){
		drawMark(2,"nom");
	}else if(message.payloadString.match(/stop/)){
		drawMark(1,"stop");
	}

	/*switch (message.destinationName) {
		//for rover-1
		case topic_base + "PicoRover/1st":
			if( message.payloadString.match(/A/) ||  message.payloadString.match(/B/) ){
				drawMark(0);
			}
		break;
		//for rover-2
		case topic_base + "PicoRover/2nd":
			if( message.payloadString.match(/A/) ||  message.payloadString.match(/B/) ){
				drawMark(1);
			}
		break;
		//for rover-3
		case topic_base + "PicoRover/3rd":
			if( message.payloadString.match(/A/) || message.payloadString.match(/B/) ){
				drawMark(2);
			}
		break;
	}*/
}

window.onload = function(){
	window.resizeTo(1400,150);

	var cw = $(".contents").width();
	var ch = $(".contents").height();

	$("#canvas").attr("width", cw);
	$("#canvas").attr("height", ch);
	
	client.onConnectionLost = onConnectionLost;
	client.onMessageArrived = onMessageArrived;
	
	client.connect({onSuccess:onConnect});
	
	//open window(s)
	w3 = window.open( "", "rover3", "width=640,height=400,top=0,left=775 resizable=0 menubar=0 location=0 toolbar=0 dependent=1");
	w2 = window.open( "", "rover2", "width=640,height=400,top=0,left=325 resizable=0 menubar=0 location=0 toolbar=0 dependent=1");
	w1 = window.open( "", "rover1", "width=640,height=400,top=0,left=0 resizable=0 menubar=0 location=0 toolbar=0 dependent=1");

	//setTitle
	w3.document.title="rover-3";
	w2.document.title="rover-2";
	w1.document.title="rover-1";

	//setURL
	w3.location.href = "http://192.168.60.16/live/index2.html?Language=1"
	w2.location.href = "http://192.168.60.18/live/index2.html?Language=1"
	w1.location.href = "http://192.168.60.17/live/index2.html?Language=1"

	//setInterval(window.focus,1000);
	drawMark(1,"stop");

}

drawMark= function(num,mode){
	var can = document.getElementById("canvas");
	var context = can.getContext("2d");

	var cw = $(".contents").width();
	var ch = $(".contents").height();

	context.clearRect(0, 0, cw, ch);
	
	if(mode == "stop"){
		context.fillStyle = "rgb(0,50,128)";
		context.fillRect(num * cw/3, 0, 0.95 * cw/3, 0.9 * ch);

		context.fillStyle = "rgb(200,128,128)";
		context.font = "bold 36px sans-serif"
		context.textAlign = "center";
		context.fillText("Not Operation", 0.95 * cw/6 + 1 * cw/3, 30, 0.9 * cw/3 );
	}else{
		context.fillStyle = "rgb(255,0,128)";
		context.fillRect(num * cw/3, 0, 0.95 * cw/3, 0.9 * ch);

		context.fillStyle = "rgb(0,0,128)";
		context.font = "bold 36px sans-serif"
		context.textAlign = "center";
		context.fillText("Now in Operation", 0.95 * cw/6 + num * cw/3, 30, 0.9 * cw/3 );
	}
	
}

