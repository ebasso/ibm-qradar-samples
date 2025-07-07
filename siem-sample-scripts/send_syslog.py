import logging
import logging.handlers

SYSLOG_IP = "192.168.1.10"
SYSLOG_PORT = 514  # Port should be an integer

def send_syslog_message(message):
    try:
        logger = logging.getLogger('SyslogLogger')
        logger.setLevel(logging.INFO)

        syslog_handler = logging.handlers.SysLogHandler(address=(SYSLOG_IP, SYSLOG_PORT))
        formatter = logging.Formatter('%(asctime)s %(name)s: %(message)s', datefmt='%b %d %H:%M:%S')
        syslog_handler.setFormatter(formatter)

        logger.addHandler(syslog_handler)
        logger.info(message)
    except Exception as e:
        print(f"Failed to send syslog message: {e}")

if __name__ == '__main__':
    message = "Teste Syslog Ebasso"
    send_syslog_message(message)