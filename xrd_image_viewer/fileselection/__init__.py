class FileSelection:
    def __init__(self, dir, sreg, preg, paths):
        self.scandir = dir
        self.scanregex = sreg
        self.pointregex = preg
        self.pointpaths = sorted(paths)

    def getscanregex(self):
        return str(self.scanregex)

    def getpointcount(self):
        return len(self.pointpaths)