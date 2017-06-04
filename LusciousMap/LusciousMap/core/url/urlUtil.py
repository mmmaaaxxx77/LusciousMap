

def getFullUrlFromName(request, urlPatterns, viewName, name):
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    for entry in urlPatterns:
        if(entry.name == name):
            return scheme + request.get_host() + "/backend/" + viewName + "/" + entry.regex.pattern.replace("^", "").replace("$", "")
    return None


def getAllFullUrl(request, urlPatterns, viewName):
    result = dict()
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'
    for entry in urlPatterns:
        result[entry.name] = scheme + request.get_host() + "/backend/" + viewName + "/" + entry.regex.pattern.replace("^", "").replace("$", "")
    return result