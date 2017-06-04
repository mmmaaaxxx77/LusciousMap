__author__ = 'mmmaaaxxx77'

def postToDic(request):
    result = dict()
    for key, value in request.POST.iteritems():
        result[key] = value[0]
    return result