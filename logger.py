from datetime import datetime
import os


class Logger:
    '''creates log files/entries
    log = Logger("log.txt", "LOG TEST")

    log.text("Message to log.")

    print last n lines of text
    log.debug(int)
    '''

    def __init__(self, filename, logging_header):
        self.filename = filename
        self.logging_header = logging_header


    def text(self, log_text):
        '''print string argument to log.filename'''

        log_line = (f"{datetime.strftime(datetime.now(),'[ %m-%d-%Y %I:%M:%S %p ]')} "\
                    f"[{self.logging_header}] {log_text} \r")

        print(log_line)
        os.makedirs(os.path.dirname('logs/'), exist_ok=True)
        log_file = open(f"logs/{self.filename}", 'a+')
        log_file.write(log_line)
        log_file.close()


    def debug(self, lines, hide_errors=False):
        '''print string argument to log.filename'''

        if not os.path.isdir("logs/"):
            print("[ DEBUG ] Logs directory not found.")
        else:
            if not os.path.isfile(f"logs/{self.filename}"):
                print("[ DEBUG ] Log file not found.")
            else:

                log_file = open(f"logs/{self.filename}", 'r')
                log_lines = log_file.readlines()

                if len(log_lines) >= lines:
                    for line in reversed(range(lines)):
                        print((f"[ DEBUG ] {log_lines[-(line+1)]}").rstrip('\n'))
                else:
                    for line in reversed(range(len(log_lines))):
                        print((f"[ DEBUG ] {log_lines[-(line+1)]}").rstrip('\n'))
                    if hide_errors is False:
                        print(f'[ DEBUG ] Unable to print {lines-len(log_lines)}/{lines}'\
                              f' requested lines. Lines in file: {len(log_lines)}')
