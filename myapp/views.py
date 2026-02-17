from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import TodoItem
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@login_required
def home(request):
    todos = TodoItem.objects.filter(user=request.user)
    return render(request, "todos.html", {"todos": todos})


@login_required
def add_todo(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        TodoItem.objects.create(
            user=request.user,
            title=title,
            description=description
        )

        return redirect("home")  # or redirect to todos page

    return render(request, "add_todo.html")



@login_required
def update_todo(request, id):
    todo = get_object_or_404(TodoItem, id=id, user=request.user)

    todo.title = request.POST.get("title")
    todo.description = request.POST.get("description")
    todo.save()

    return JsonResponse({"status": "updated"})


@login_required
def delete_todo(request, id):
    todo = get_object_or_404(TodoItem, id=id, user=request.user)
    todo.delete()
    return JsonResponse({"status": "deleted"})


@login_required
def toggle_complete(request, id):
    todo = get_object_or_404(TodoItem, id=id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return JsonResponse({"completed": todo.completed})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# REST API
class TodoListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        todos = TodoItem.objects.filter(user=request.user)
        data = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
            }
            for t in todos
        ]
        return Response(data)






