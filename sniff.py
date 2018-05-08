import sys, pyshark


def generate_pcap_files(interface, timeout, output_file):
    capture = pyshark.LiveCapture(output_file=output_file, interface=interface)

    print('Capture packets', timeout, output_file)
    capture.sniff(timeout=timeout)
    print('Packets Captured', capture)


def run(interface, env):
    print('----------------------------------------')

    for j in range(40):
        timeout = 10 * (env+1) * (j%4+1 + 1)
        filename = 'env_' + str(env) + '_setting_' + str(j) + '.pcap'
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
