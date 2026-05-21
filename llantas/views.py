from django.shortcuts import render
from .algoritmo import buscar_solucion


def inicio(request):

    contexto = {}

    # PASO 1
    if request.method == 'POST' and 'generar' in request.POST:

        num_tipos = int(
            request.POST.get('num_tipos')
        )

        num_empresas = int(
            request.POST.get('num_empresas')
        )

        contexto = {
            'num_tipos': range(num_tipos),
            'num_empresas': range(num_empresas),
            'mostrar_formulario': True
        }

    # PASO 2
    elif request.method == 'POST' and 'calcular' in request.POST:

        tipos = request.POST.getlist('tipos')

        empresas = request.POST.getlist('empresas')

        tabla_costos = {}

        for empresa in empresas:

            tabla_costos[empresa] = {}

            for tipo in tipos:

                nombre = f"{empresa}_{tipo}"

                costo = int(
                    request.POST.get(nombre)
                )

                tabla_costos[empresa][tipo] = costo

        nodo_solucion = buscar_solucion(
            empresas,
            tipos,
            tabla_costos
        )

        resultado = []

        total = 0

        for empresa, tipo in nodo_solucion.get_datos():

            costo = tabla_costos[empresa][tipo]

            total += costo

            resultado.append({
                'empresa': empresa,
                'tipo': tipo,
                'costo': costo
            })

        contexto = {
            'resultado': resultado,
            'total': total
        }

    return render(
        request,
        'index.html',
        contexto
    )