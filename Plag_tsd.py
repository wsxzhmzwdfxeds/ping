from otsdb_client import client
import os,time,logging
logger = logging.getLogger("lag")
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
logger.setLevel(logging.INFO)

class ping_lag(object):
    def __init__(self):
        self.std_client = client.Connection('10.19.140.200', 30142)
        self.ip_list = ['10.19.140.4','10.19.140.7','10.19.140.8','10.19.140.9','10.19.138.119','10.19.138.36']
        for i in range(140,160):
            self.ip_list.append('10.19.137.%d' % i)

    def _run(self):
        for ip in self.ip_list:
            ping_str = os.popen("ping %s -c 5" % ip).read()
            logger.info(ping_str)
            try:
                avg_lag = ping_str.splitlines()[-1].split('/')[4]
            except IndexError as e:
                logger.exception("index error")
            else:
                self._to_std(avg_lag, self._get_ip(), ip)

    def _to_std(self, value, from_ip, to_ip):
        logger.info("from %s to %s , and the value is %s" % (from_ip,to_ip,value))
        self.std_client.put(metric='icy_lag', values=[value],tags={"from":from_ip,"to":to_ip})
    def _get_ip(self):
        # return os.popen('echo $HOST_IP').read().strip()
        return "10.19.138.138"

pl = ping_lag()
while True:
    pl._run()
    time.sleep(20)
    logger.info("waiting for 20s")