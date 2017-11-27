import pings
import paho.mqtt.client as mqtt

hosts = ["192.168.95.212", "192.168.95.213", "192.168.95.214"]
topics = ["1st","2nd","3rd"]

p = pings.Ping(packet_size=600) # Pingオブジェクト作成

throughput = 0

host = "127.0.0.1"
port = 1883
topic = 'PicoRover/throughput/'


client = mqtt.Client(protocol=mqtt.MQTTv311)
client.connect(host, port=port, keepalive=60)
print ("on_connect")

while(1):
	i = 0
	for h in hosts:
		res = p.ping(h)
		if res.is_reached():
			# 監視対象への接続ができた
			print("")
			throughput = res.packet_size*2*8/res.avg_rtt/1000
			print("throughput = {0} Mbps".format(throughput))
			res.print_messages()  # メッセージが表示される
			client.publish(topic + topics[i],"{0} Mbps".format(throughput))
		else:
			# 監視対象への接続ができなかった
			print("")
			print("接続ができなかった")
		i = i + 1