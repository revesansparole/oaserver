from oaserver.watchdog import Watchdog, WatchdogListener


class LogWatch(WatchdogListener):
    def __init__(self):
        pass

    def file_created(self, name, cnt):
        print name, cnt


log = LogWatch()
w = Watchdog("dirac:/vo.france-grilles.fr/user/j/jchopard/tata", log)
w.start()
