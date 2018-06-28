from oyoyo.client import IRCClient
from oyoyo.parse import parse_nick
import logging
import botconfig
import time
import traceback
import modules.common
import sys

class UTCFormatter(logging.Formatter):
    converter = time.gmtime

def main():
    if not botconfig.DEBUG_MODE:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("errors.log")
        fh.setLevel(logging.WARNING)
        logger.addHandler(fh)
        if botconfig.VERBOSE_MODE:
            hdlr = logging.StreamHandler(sys.stdout)
            hdlr.setLevel(logging.DEBUG)
            logger.addHandler(hdlr)
        formatter = UTCFormatter('[%(asctime)s] %(message)s', '%d/%b/%Y %H:%M:%S')
        for handler in logger.handlers:
            handler.setFormatter(formatter)
    else:
        logging.basicConfig(level=logging.DEBUG)
        formatter = UTCFormatter('[%(asctime)s] %(message)s', '%H:%M:%S')
        for handler in logging.getLogger().handlers:
            handler.setFormatter(formatter)
    
    cli = IRCClient(
                      {"privmsg":modules.common.on_privmsg,
                       "notice":lambda a, b, c, d: modules.common.on_privmsg(a, b, c, d, True),
                       "":modules.common.__unhandled__},
                     host=botconfig.HOST, 
                     port=botconfig.PORT,
                     authname=botconfig.USERNAME,
                     password=botconfig.PASS,
                     nickname=botconfig.NICK,
                     sasl_auth=botconfig.SASL_AUTHENTICATION,
                     use_ssl=botconfig.USE_SSL,
                     connect_cb=modules.common.connect_callback
                    )
    cli.mainLoop()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.error(traceback.format_exc())
