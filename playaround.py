from rtmom import *
# playing around
def printTasks(rtm):
    """
    Command line output of all tasksk for testing purposes
    """
#    for task in getTasks(rtm):
    for task in getTasks(rtm, "Privat"):
        print task

def printCategories(rtm):
    for cat in getCategories(rtm):
        print cat

        
if __name__ == '__main__':
    c = getConnection()
    printCategories(c)
    print "\n\n"
    printTasks(c)
