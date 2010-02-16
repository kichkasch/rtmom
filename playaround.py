def playWithConnections():
    import rtmom_net
    net = rtmom_net.getInternetConnector()
    net.connect()
#
#    tl = net._connection.timelines.create().timeline
#    print tl

    
    cats = net.loadCategories()
    
    t = {}
    for key, cat in cats.iteritems():
        print "Kategorie: %s, %s" %(key, cat)
        tasks = net.loadFullTasks(cat)
        for task in tasks:
            print "\t%s" %(task.name)
        
#    cat = cats.keys()[0]
#    task = t[cat][0]
#    print "Marking finished: "
#    print "\tCat: " + cat
#    print "\tTasks: " + task.name
#        
#    net.markTaskCompleted(cats[cat], task)

def playWithConfig():
    import config
    config.getSettings()
    print config.getSettings().getValue("hidden_groups",  list)
    print config.getSettings().getValue("show_completed", bool)

if __name__ == '__main__':
#    playWithConnections()
    playWithConfig()
