1. Download chromedriver and note path to chromedriver
2. Install chromium-browser. Command: - sudo apt-get install chromium-browser
2. Install all the python requirements. Command: sudo pip install -r requirements.txt
3. Check network interface using ifconfig and note it.
4. Get hostname and server port.
5. Env = 1 to 8.
6. Update network setting using setNetwork.py. Command: python setNetwork out_interface in_interface env
7. To get page load time run getRequest.py. Command: python getRequest hostname server_port path_to_chromedriver env