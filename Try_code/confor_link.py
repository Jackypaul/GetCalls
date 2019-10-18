links = ["http://ok.com/en","https://ok.com/en","ok.com","www.ok.com","http://www.ok.com/","http://www.ok.xom","www.ok.com","www.ok.com/en"]

def conform_link(link):
    ret =''
    linkp = link.split('/')
    for part in linkp:
        part =str(part)
        if (part.startswith('www.', 0, 5)):
            return (part)
        else:
            for l in part:
                if (l == '.'):
                    if (part.startswith('www.', 0, 5)):
                        return (part)
                    else:
                        return ("www."+part)
    return (ret)

for link in links:
    print conform_link(str(link))
