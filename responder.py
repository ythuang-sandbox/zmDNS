#!/usr/bin/env python

import zmq
import msgpack
import netutils

ip = netutils.get_ip("eth0")
print "ip is ",ip
def wait_query():
    context = zmq.Context()
    query_socket = context.socket(zmq.SUB)
    query_socket.bind("pgm://%s;224.0.0.1:5555", ip)
    query_socket.setsockopt(zmq.SUBSCRIBE, '')
    while True:
        msg = query_socket.recv()
        query_msg = msgpack.unpackb(msg)

        if 'query' == query_msg['message']:
            reply_ip = query_msg['ip']
            reply_socket = context.socket(zmq.REQ)
            reply_socket.connect("tcp://%s:5556" % reply_ip)
            reply_msg = {"ip": "%s" % ip, "message": "reply"}
            reply_socket.send(msgpack.packb(reply_msg))
            msg = reply_socket.recv()
            ack_msg = msgpack.unpackb(msg)
            print "got the message from query agent: ", ack_msg['message']

            reply_socket.close()

    query_socket.close()

if __name__ == '__main__':
    wait_query()