from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from rest_framework import viewsets

from .models import *
from social_network import filters
from social_network import serializers


class UserAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.User


class MessageAPI(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = serializers.Message


class UserListView(FilterView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
    filterset_class = filters.UserFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.get_filterset(filters.UserFilter)
        return context


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'


class UserCreateView(CreateView):
    model = User
    template_name = 'user_form.html'
    fields = ['first_name', 'last_name', 'email', 'avatar', 'date_of_birth']

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.object.pk})


class UserUpdateView(UpdateView):
    model = User
    template_name = 'user_form.html'
    fields = ['first_name', 'last_name', 'email', 'avatar', 'date_of_birth']

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

