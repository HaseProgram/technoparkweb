from django.http import HttpResponse

def helloworld(request):
    output = '<h2>Hello World!</h2>'
    if request.method == 'GET':
        if len(request.GET):
            output += '<b>GET request data</b>: <br>'
            for data in request.GET:
                output += data
                output += ' = '
                output += request.GET[data]
                output += '<br>'
    if request.method == 'POST':
        output += '<b>POST request data</b>: <br>'
        for data in request.POST:
            output += data
            output += ' = '
            output += request.POST[data]
            output += '<br>'
    return HttpResponse(output)
