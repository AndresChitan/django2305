from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tarea(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null = True, blank = True)

    completo = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    #definir el valor para que nos imprima la tarea
    def __str__(self):
        return self.titulo
    #ordenar las tareas de la tabla, las ordenamos por 
    #tarea completada
    class meta: odering = ['completado']

