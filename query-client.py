#!/usr/bin/env python

import zmq
import msgpack
import netutils
import time

# https://code.google.com/p/tx0mq/source/browse/examples/pyzmq/poll/reqrep.py

def query_host(ifname, timeout=10):
    """
    Query hosts on network given an interface name
    parameters:
        ifname: interface to use for query
        timeout: optional, defaults to 10 seconds
    returns:
        return a list of host ip addresses
    exceptions:
        if interface name is invalid, InvalidIFName exception is raised
    """

    ip = netutils.get_ip(ifname)
    context = zmq.Context()
    query_socket = context.socket(zmq.PUB)
    reply_socket = context.socket(zmq.REP)
    query_socket.bind("pgm://%s;224.0.0.2:5555" % ip)

    reply_socket.bind("tcp://%s:5556" % ip)

    query_msg = {"ip": "%s" % ip, "message": "query"}
    query_socket.send(msgpack.packb(query_msg))
    print "sending message ", query_msg

    poller = zmq.Poller()
    poller.register(reply_socket, zmq.POLLIN)

    hosts = []
    for c in range(1, timeout):
        socks = dict(poller.poll(1))
        if reply_socket in socks and socks[reply_socket] == zmq.POLLIN:
            msg = reply_socket.recv()
            ack_msg = {"ip": "%s" % ip, "message": "ok"}
            reply_socket.send(msgpack.packb(ack_msg))
            reply_msg = msgpack.unpackb(msg)
            hosts.append(reply_msg['ip'])
        print "waiting ", c
        time.sleep(1)

    query_socket.close()
    reply_socket.close()

    return hosts

if __name__ == '__main__':
    h = query_host("eth0")
    print "got list of host: ", h