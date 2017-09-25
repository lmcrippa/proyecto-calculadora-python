from django.db import models


class Sesion (models.Model):
    nombre = models.CharField(max_length=20)
    fecha = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.nombre


class Calculo (models.Model):
    operacion = models.CharField(max_length=200)
    resultado = models.CharField(max_length=20)
    Sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.operacion, ' = ', self.resultado)
