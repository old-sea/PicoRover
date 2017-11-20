import pings

hosts = ["192.168.95.106", "10.10.227.62", "192.168.95.106"]

p = pings.Ping(packet_size=600) # Pingオブジェクト作成

throughput = 0

for h in hosts:
	res = p.ping(h)
	if res.is_reached():
		# 監視対象への接続ができた
		throughput = res.packet_size*2*8/res.avg_rtt/1000
		print("throughput = {0} Mbps".format(throughput))
		res.print_messages()  # メッセージが表示される
	else:
		# 監視対象への接続ができなかった
		print("接続ができなかった")