Start Your Local Servers:
1. HTTP/1.1
$node server.js
2. HTTP/2 :
a) $ws --htp2
b) $node --expose-http2 server2.js
3. SPDY:
$node app.js

1. Download chromedriver and note path to chromedriver
2. Install all the python requirements. Command: sudo pip install -r requirements.txt
3. Check network interface using ifconfig and note it.
4. Get hostname and server port.
5. Run the generatePCAP.py. Command: sudo python interface_name hostname server_port path_to_chromedriver
