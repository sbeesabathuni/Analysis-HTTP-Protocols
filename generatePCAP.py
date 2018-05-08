import os, sys, pyshark
from multiprocessing import Process
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import subprocess
import time
import requests
from threading import Thread
from time import sleep

def set_start_request(start_get_request):
    start_get_request = False

def set_ingress_interface(interface):
    # Initial Setup
    os.system('sudo modprobe ifb')
    os.system('sudo ip link set dev ifb0 up')
    os.system('sudo tc qdisc add dev {} ingress'.format(interface))
    os.system('sudo tc filter add dev {} parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0'.format(interface))


# Sample: net_env = {'delay': '94ms', 'loss': '10%', 'rate': '1024kbit', 'latency': '50ms', 'burst': '1540'}
def set_net_environment(interface, net_env):
    delay = net_env['delay']
    loss = net_env['loss']

    if 'rate' not in net_env:
        os.system('sudo tc qdisc add dev {} root netem delay {} loss {}'.format(interface, delay, loss))
        print('Net setting: ', subprocess.check_output('sudo tc qdisc show dev {}'.format(interface), shell=True))
        return

    rate = net_env['rate']
    latency = net_env['latency']
    burst = net_env['burst']

    # Set loss and delay
    os.system('sudo tc qdisc add dev {} root handle 1:0 netem delay {} loss {}'.format(interface, delay, loss))
    # Set rate limit
    os.system('sudo tc qdisc add dev {} parent 1:1 handle 10: tbf rate {} latency {} burst {}'.format(interface, rate, latency, burst))
    print('Net setting: ', subprocess.check_output('sudo tc qdisc show dev {}'.format(interface), shell=True))


def generate_pcap_files(output_file, interface, timeout, driver, hostname, server_port, web_env):
    # Capture packets - Thread 1
    capture = pyshark.LiveCapture(output_file=output_file, interface=interface)

    print('Start thread')
    thread = Thread(target=get_request, args=(driver, hostname, server_port, web_env,))
    thread.start()
    print('Capture packets...')
    capture.sniff(timeout=timeout)
    print('Packets Captured', capture)
    thread.join()
    print("Thread finished...exiting")

# def get_clear_browsing_button(driver):
#     # Find the "CLEAR BROWSING BUTTON" on the Chrome settings page.
#     return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


# def clear_cache(driver, timeout=60):
#     # Clear the cookies and cache for the ChromeDriver instance
#     # Navigate to the settings page
#     driver.get('chrome://settings/clearBrowserData')
#     # Wait for the button to appear
#     wait = WebDriverWait(driver, timeout)
#     wait.until(get_clear_browsing_button)
#     # Click the button to clear the cache
#     get_clear_browsing_button(driver).click()
#     # Wait for the button to be gone before returning
#     wait.until_not(get_clear_browsing_button)


def get_request(driver, hostname, server_port, web_env):
    # clear_cache(driver)
    sleep(10)

    url = 'http://' + hostname + ':' + server_port + '/' + web_env
    # print(url)
    print('Get Request')
    # driver.get(url)
    requests.get(url, headers={'Cache-Control': 'no-cache'})
    # webbrowser.open_new_tab(url)
    print('Request Finished')


def run(interface, hostname, server_port, chromedriver_path):
    set_ingress_interface(interface)
    net_settings = {'env1': {'delay': '20ms', 'loss': '0%'},
                    'env2': {'delay': '200ms', 'loss': '0%'},
                    'env3': {'delay': '20ms', 'loss': '2%'},
                    'env4': {'delay': '200ms', 'loss': '2%'},
                    'env5': {'delay': '20ms', 'loss': '0%', 'rate': '5mbit', 'latency': '50ms', 'burst': '1540'},
                    'env6': {'delay': '200ms', 'loss': '0%', 'rate': '5mbit', 'latency': '50ms', 'burst': '1540'},
                    'env7': {'delay': '20ms', 'loss': '2%', 'rate': '5mbit', 'latency': '50ms', 'burst': '1540'},
                    'env8': {'delay': '200ms', 'loss': '2%', 'rate': '5mbit', 'latency': '50ms', 'burst': '1540'}}

    print('Starting chrome browser. Path: {}'.format(chromedriver_path))
    # browser = webdriver.Chrome(chromedriver_path)
    browser = ''
    web_settings = {'env1': 'lessobjectslesssize',
                    'env2': 'moreobjectslesssize',
                    'env3': 'lessobjectsmoresize',
                    'env4': 'moreobjectsmoresize'}

    print('----------------------------------------')
    for i in range(1, 9):
        set_net_environment(interface, net_settings['env' + str(i)])

        for j in range(1, 5):
            print('----------------------Setting {}{}----------------------'.format(i, j))
            print('Net Setting: ', net_settings['env' + str(i)])
            print('Web Setting: ', web_settings['env' + str(j)])
            timeout = 10 * i * (j+1) + 10
            for k in range(10):
                filename = 'env_' + str(k) + '_setting_' + str(i) + str(j) + '.pcap'
                generate_pcap_files(filename, interface, timeout, browser, hostname, server_port, web_settings['env' + str(j)])
                # p1 = Process(target=generate_pcap_files, args=(filename, interface, timeout))
                # p1.start()
                # # get_request(browser, web_settings['env' + str(j)])
                # p2 = Process(target=get_request, args=(browser, hostname, server_port, web_settings['env' + str(j)],))
                # p2.start()
                # p1.join()
                # p2.join()

        # Delete network setup
        print('Deleting network setup')
        os.system('sudo tc qdisc del dev {} root'.format(interface))
        print('----------------------------------------')


# def start_test():
#     interface = 'enp0s3'
#     hostname = '172.24.24.93'
#     server_port = '8080'
#     chromedriver_path = '/opt/chromedriver'
#
#     print('Start generating PCAP files.....')
#     run(interface, hostname, server_port, chromedriver_path)
#     print('Generated PCAP files!!!')


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print('Incorrect command')
        sys.exit(1)

    interface = sys.argv[1]
    hostname = sys.argv[2]
    server_port = sys.argv[3]
    chromedriver_path = sys.argv[4]

    print('Start generating PCAP files.....')
    run(interface, hostname, server_port, chromedriver_path)
    print('Generated PCAP files!!!')
