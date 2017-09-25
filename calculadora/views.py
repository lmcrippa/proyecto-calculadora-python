from django.shortcuts import render, get_object_or_404
from calculadora.models import Calculo, Sesion
import math

calculos_list = []


def index(request):
    sesiones = Sesion.objects.all().order_by('-fecha')
    res = ''
    if request.method == 'POST':
        #la accion post a realizar es calcular
        if request.POST.get("btn_calcular"):
            operacion_post = request.POST['operacion']
            '''reemplaza la palabra log por math.log 
            para que pueda ser calculada por dicha libreria'''
            operacion = operacion_post.replace("log", "math.log")
            try:
                #obtencion de la evaluacion de la operacion recibida
                res = eval(str(operacion))
                calc = [operacion_post, res]
                #agrega la operacion con su resultado a la lista de calculos
                calculos_list.append(calc)
            except ZeroDivisionError:
                res = 'Error: División por cero'
            except Exception:
                res = 'Error: Operación incorrecta'
        #la accion post a realizar es guardar
        elif request.POST.get("btn_guardar"):
            nombre_post = request.POST['nombre_sesion']
            sesion = Sesion(nombre=nombre_post)
            sesion.save()
            for calc_corr in calculos_list:
                #nuevo calculo a almacenar
                c = Calculo(operacion=str(calc_corr[0]), resultado=str(calc_corr[1]), Sesion=sesion)
                c.save()
            #elimina los elementos de la lista ya que fueron almacenados
            del calculos_list[:]
            #actualiza el elemento sesiones por la nueva sesion almacenada
            sesiones = Sesion.objects.all().order_by('-fecha')
    return render(request, 'index.html', {'sesiones': sesiones, 'resultado': res, })


def sesion_detalle(request, sesion_id):
    #obtencion de la sesion cuyo id es sesion_id
    sesion = get_object_or_404(Sesion, pk=sesion_id)
    #obtencion de los calculos asociados a la sesion anterior
    calculos_sesion = Calculo.objects.filter(Sesion_id=sesion.id)
    return render(request, 'sesion_detalle.html', {'calculos': calculos_sesion, 'sesion': sesion, })
