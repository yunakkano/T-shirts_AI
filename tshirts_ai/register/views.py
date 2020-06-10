from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.views.generic.edit import CreateView


class SignUp(CreateView):
    form_class = RegisterForm
    template_name = "register/register.html" 
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        login(self.request, user) # 認証
        self.object = user 
        return HttpResponseRedirect(self.get_success_url()) # リダイレクト


# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect("/")
#     else:
#         form = RegisterForm()

#     return render(request, "register/register.html", {"form": form})


