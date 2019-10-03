from scapy.all import *

def process_packet(pkt: Ether):
    pkt.show()


def main():
    pkts = sniff(iface="en0", prn=process_packet)


if __name__ == '__main__':
    main()
