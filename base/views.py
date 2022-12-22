from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView
from base.tokens import account_activation_token

from base.models import Task
from base.tokens import account_activation_token
# from django.utils.encoding import force_text

#
# class ActivateAccount(View):
#     def get(self, request, uidb64, token, *args, **kwargs):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#
#         if user is not None and account_activation_token.check_token(user, token):
#             user.is_active = True
#             user.profile.email_confirmed = True
#             user.save()
#             login(request, user)
#             messages.success(request, ('Your account have been confirmed.'))
#             return redirect('tasks')
#         else:
#             messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
#             return redirect('tasks')


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterView, self).get(*args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.is_active = False  # Deactivate account till it is confirmed
    #         user.save()
    #
    #         current_site = get_current_site(request)
    #         subject = 'Activate Your MySite Account'
    #         message = render_to_string('emails/account_activation_email.html', {
    #             'user': user,
    #             'domain': current_site.domain,
    #             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #             'token': account_activation_token.make_token(user),
    #         })
    #         user.email_user(subject, message)
    #
    #         messages.success(request, ('Please Confirm your email to complete registration.'))
    #
    #         return redirect('login')
    #
    #     return render(request, self.template_name, {'form': form})


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__contains=search_input)
        context['search_input'] = search_input
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    #
    # def f(self, form):
    #     return super(TaskCreateView).form_valid(form)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    fields = ['title', 'description', 'complete']


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

#
# class TaskReorder(View):
#     def post(self, request):
#         form = PositionForm(request.POST)
#
#         if form.is_valid():
#             positionList = form.cleaned_data["position"].split(',')
#
#             with transaction.atomic():
#                 self.request.user.set_task_order(positionList)
#
#         return redirect(reverse_lazy('tasks'))
