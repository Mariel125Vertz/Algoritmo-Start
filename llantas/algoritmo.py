from .arbol import Nodo


def heuristica(empresas_restantes,
               tipos_restantes,
               tabla_costos):

    h = 0

    for tipo in tipos_restantes:

        menor = float('inf')

        for empresa in empresas_restantes:

            costo = tabla_costos[empresa][tipo]

            if costo < menor:
                menor = costo

        h += menor

    return h


def buscar_solucion(empresas,
                    tipos,
                    tabla_costos):

    solucionado = False

    nodos_visitados = []
    nodos_frontera = []

    nodo_inicial = Nodo([])

    nodo_inicial.set_costo(0)

    nodos_frontera.append(nodo_inicial)

    while (not solucionado) and len(nodos_frontera) != 0:

        nodos_frontera.sort(
            key=lambda nodo:
            nodo.get_costo() +
            heuristica(
                [
                    e for e in empresas
                    if e not in [
                        x[0]
                        for x in nodo.get_datos()
                    ]
                ],
                tipos[len(nodo.get_datos()):],
                tabla_costos
            )
        )

        nodo = nodos_frontera.pop(0)

        nodos_visitados.append(nodo)

        if len(nodo.get_datos()) == len(tipos):

            solucionado = True
            return nodo

        else:

            asignaciones = nodo.get_datos()

            tipo_actual = tipos[
                len(asignaciones)
            ]

            empresas_usadas = [
                x[0]
                for x in asignaciones
            ]

            empresas_restantes = [
                e for e in empresas
                if e not in empresas_usadas
            ]

            lista_hijos = []

            for empresa in empresas_restantes:

                nueva_asignacion = (
                    asignaciones.copy()
                )

                nueva_asignacion.append(
                    (empresa, tipo_actual)
                )

                hijo = Nodo(
                    nueva_asignacion
                )

                hijo.set_padre(nodo)

                costo_actual = (
                    nodo.get_costo()
                )

                costo_rueda = (
                    tabla_costos
                    [empresa][tipo_actual]
                )

                hijo.set_costo(
                    costo_actual +
                    costo_rueda
                )

                lista_hijos.append(hijo)

                if not hijo.en_lista(
                    nodos_visitados
                ):

                    if not hijo.en_lista(
                        nodos_frontera
                    ):

                        nodos_frontera.append(
                            hijo
                        )

            nodo.set_hijos(lista_hijos)

    return None