import netifaces

class InvalidIFName(Exception):
    pass

def get_ip(ifname):
    """
    Get ip given if name
    raises InvalidIFName if provided ifname is not a valid interface name
    """
    if ifname not in netifaces.interfaces():
        raise InvalidIFName("Invalid IFName %s" % ifname)

    ip = netifaces.ifaddresses(ifname)[netifaces.AF_INET][0]['addr']

    return ip