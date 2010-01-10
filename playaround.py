        
if __name__ == '__main__':
    import rtmom_net
    net = rtmom_net.getInternetConnector()
    net.connect()
#
#    tl = net._connection.timelines.create().timeline
#    print tl

    
    cats = net.loadCategories()
    
    t = {}
    for cat in cats.keys():
        t[cat] = net.loadFullTasks(cats[cat])
        
    cat = cats.keys()[0]
    task = t[cat][0]
    print "Marking finished: "
    print "\tCat: " + cat
    print "\tTasks: " + task.name
        
    net.markTaskCompleted(cats[cat], task)
