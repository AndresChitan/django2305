from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin #Para que no se pueda acceder a la vista sin loguearse
from django.urls import reverse_lazy
from . models import Tarea


# Create your views here.

class Logueo(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tareas') #Cuando termine tiene que ir a esa página (que lo devuelve al listado de tareas)
    
class PaginaRegistro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tareas')
    
    def form_valid(self, form):
        usuario= form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form) #llama a la función form_valid de la clase padre (FormView)

        
class ListaPendientes(LoginRequiredMixin,ListView):
    model = Tarea
    context_object_name = 'tareas'
    
# get_context se tiene una vista basada en la clase para modificar o ampliar el contexto
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tareas'] = context['tareas'].filter(usuario=self.request.user) #el metodo self es para acceder a la clase
    context['count'] = context['tareas'].filter(completo=False).count() #cuenta las tareas que no están completadas
    return context


class DetalleTarea(LoginRequiredMixin,DetailView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'base/tarea.html'

class CrearTarea(LoginRequiredMixin,CreateView):
    model = Tarea
    fields = ['titulo','descripcion','completo']
    success_url = reverse_lazy('tareas')
    
    #funcion (form_valid) que se ejecuta cuando el formulario es válido
    #se usa para asignar el usuario a la tarea
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearTarea.self).form_valid(form)

class EditarTarea(LoginRequiredMixin,UpdateView):
    model = Tarea
    fields = ['titulo','descripcion','completo']
    success_url = reverse_lazy('tareas')

class EliminarTarea(LoginRequiredMixin,DeleteView):
    model = Tarea
    context_object_name = 'tarea'
    success_url = reverse_lazy('tareas')
    template_name = 'base/tarea_confir_delete.html'




