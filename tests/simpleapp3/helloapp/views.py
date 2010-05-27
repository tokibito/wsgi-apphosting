from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello Django!', content_type='text/plain')
