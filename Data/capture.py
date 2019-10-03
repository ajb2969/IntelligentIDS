import netifaces

from scapy.all import *
from scapy.layers.l2 import Ether


class InterfaceListen(Thread):
    """docstring for Interface_Listen."""

    def __init__(self, interface_name, outputfile):
        self.lock = threading.Lock()
        self.interface = interface_name
        self.output = sys.stdout
        self.outputfile = outputfile
        super(InterfaceListen, self).__init__()

    def run(self):
        with self.lock:
            self.output.write("Starting to listen on interface: " + self.interface + "\n")
        self.interface_listener()

    def interface_listener(self):
        with self.lock:
            self.output.write("Starting thread for " + self.interface + "\n")
        sniff(iface="en0", prn=self.process_packet, count=10)

    def process_packet(self, pkt: Ether):
        with self.lock:
            with open(self.outputfile, "a") as f:
                # Flags, protocol, payload, packet id, source/dest ports, timestamps?
                f.write(pkt.__str__())
                f.write("\n")
                f.flush()


def main():
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print("Usage: python3 capture.py <output file>")
    else:
        threads = []
        for interface in netifaces.interfaces():
            try:
                # sniff packets from one or more interfaces
                threads.append(InterfaceListen(interface, sys.argv[1]))
            except IOError:
                print("Unable to create thread for interface: ", interface)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == '__main__':
    main()