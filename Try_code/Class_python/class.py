class Test():
    arg = []
    def __init__(self,arg):
        self.arg = arg

    def start(self):
        print "in start"
        while(self.arg):
            print self.arg.pop()
            
t = Test(["The","list","methods","make","it","very","easy","to","use"])
t.start()
