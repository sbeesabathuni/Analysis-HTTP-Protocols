import os, sys
import subprocess


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


def run(interface, env):
    # Delete network setup
    print('Deleting network setup')
    os.system('sudo tc qdisc del dev {} root'.format(interface))

    set_ingress_interface(interface)
    net_settings = {'env1': {'delay': '20ms', 'loss': '0%'},
                    'env2': {'delay': '200ms', 'loss': '0%'},
                    'env3': {'delay': '20ms', 'loss': '2%'},
                    'env4': {'delay': '200ms', 'loss': '2%'},
                    'env5': {'delay': '20ms', 'loss': '0%', 'rate': '5mbit', 'latency': '50ms', 'burst': '1540'},
                    'env6': {'delay': '200ms', 'loss': '0%', 'rate': '5mbit', 'latency': '50ms', 'burst': '1540'},
                    'env7': {'delay': '20ms', 'loss': '2%', 'rate': '5mbit', 'latency': '50ms', 'burst': '1540'},
                    'env8': {'delay': '200ms', 'loss': '2%', 'rate': '5mbit', 'latency': '50ms', 'burst': '1540'}}


    print('----------------------------------------')
    set_net_environment(interface, net_settings['env' + str(env)])
    print('Net Setting: ', net_settings['env' + str(env)])
    print('----------------------------------------')


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Incorrect command')
        sys.exit(1)

    interface = sys.argv[1]
    env = sys.argv[2]
    run(interface, env)
