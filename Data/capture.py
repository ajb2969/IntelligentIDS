from threading import Barrier, Thread
import netifaces
import sys

from scapy.all import *

class Interface_Listen(Thread):
    """docstring for Interface_Listen."""

    def __init__(self, interface_name, outputfile):
        self.lock = threading.Lock()
        self.interface = interface_name
        self.outputfile = outputfile
        super(Interface_Listen, self).__init__()

    def run(self):
        print("Starting to listen on interface: ", self.interface)
        self.interface_listener()

    def interface_listener(self):
        print("Starting thread for ", self.interface)
        sniff(iface="en0", prn=self.process_packet, count=10)

    def process_packet(self, pkt: Ether):
            self.lock.acquire()
            with open(self.outputfile, "a") as f:
                f.write(pkt.summary() + "\n")
            self.lock.release()


def main():
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print("Usage: python3 capture.py <output file>")
    else :
        threads = []
        for interface in netifaces.interfaces():
            print("got interface", interface)
            try:
                # sniff packets from one or more interfaces
                threads.append(Interface_Listen(interface, sys.argv[1]))
            except:
                print("Unable to create thread for interface: ", interface)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == '__main__':
    main()
