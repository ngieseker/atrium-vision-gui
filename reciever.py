import lcm
import multiprocessing
from crew import report
from Queue import Empty
from time import sleep




class Data(object):
    """Class made to handle messages. Uses a pipe to transmit the messages"""
    lc = lcm.LCM()
    pipe = 0

    # Constructor takes a send pipe
    def __init__(self, d ):
        self.pipe = d

    def port(self, channel, data):
        """Recieves the message and sends it through the pipe"""
        msg = report.decode(data)
        self.pipe.send((msg.name, msg.message))

        
def recieve(p):
    """Repeatedly runs the function to handle messages recieved"""
    inara = Data(p)
    subscription = inara.lc.subscribe("EXAMPLE", inara.port)
    try:
        while True:
            inara.lc.handle()
    except KeyboardInterrupt:
        pass

# Was Used for testing purposes when a queue was used, no longer useful
def p(queue):
    """Prints what is in the queue"""
    try:
        while True:
            try:
                msg = queue.get(0)
                print str(msg[0]), ' ', str(msg[1])
            except Empty:
                pass
    except KeyboardInterrupt:
        pass

