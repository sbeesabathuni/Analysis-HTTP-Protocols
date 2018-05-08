import sys, pyshark
import time


def generate_pcap_files(interface, timeout, output_file):
    capture = pyshark.LiveCapture(output_file=output_file, interface=interface)

    print('Capture packets', timeout, output_file)
    capture.sniff(timeout=timeout)
    print('Packets Captured', capture)


def run(interface, env):
    print('----------------------------------------')

    for j in range(1, 5):
        for k in range(5):
            print('--------------{}{}------------------------'.format(j, k))
            timeout = 10 * (env+1) * (j + 1)
            filename = 'env_' + str(k) + '_setting_' + str(env) + str(j) + '.pcap'
            print('Timestamp ', time.time())
            generate_pcap_files(interface, timeout, filename)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Incorrect command')
        sys.exit(1)

    interface = sys.argv[1]
    env = int(sys.argv[2])
    print('Start generating PCAP files.....')
    run(interface, env)
    print('Generated PCAP files!!!')
