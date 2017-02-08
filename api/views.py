from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'api/index.html', context)
def landmark(request):
    context={'list': ['Kerckhoff Hall', 'Powell Library']}
    return render(request, 'api/landmark_list.html', context) 
