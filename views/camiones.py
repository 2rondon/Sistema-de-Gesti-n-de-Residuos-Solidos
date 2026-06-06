import flet as ft
from database import crear_camion, obtener_camiones, eliminar_camion

def CamionesView(page: ft.Page):
    # Campos de texto
    txt_placa = ft.TextField(label="Placa del Camión", width=200, hint_text="ABC-123X")
    txt_modelo = ft.TextField(label="Modelo / Marca", width=250)
    txt_capacidad = ft.TextField(label="Capacidad (Toneladas)", width=180, value="0.0")
    
    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Placa")),
            ft.DataColumn(ft.Text("Modelo")),
            ft.DataColumn(ft.Text("Capacidad (Ton)")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def actualizar_tabla():
        tabla_datos.rows.clear()
        for c in obtener_camiones():
            camion_id, placa, modelo, capacidad, estado = c
            tabla_datos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(placa)),
                        ft.DataCell(ft.Text(modelo)),
                        ft.DataCell(ft.Text(f"{capacidad} Ton")),
                        ft.DataCell(ft.Text(estado, color="green" if estado == "Activo" else "orange")),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINE,
                                icon_color="red400",
                                data=camion_id,
                                on_click=btn_eliminar_click
                            )
                        ),
                    ]
                )
            )
        try:
            tabla_datos.update()
        except Exception:
            pass

    def btn_guardar_click(e):
        if not txt_placa.value or not txt_modelo.value:
            mostrar_snack("Por favor, llena los campos obligatorios.")
            return
        try:
            capacidad = float(txt_capacidad.value)
        except ValueError:
            mostrar_snack("La capacidad debe ser un número válido.")
            return

        if crear_camion(txt_placa.value.upper(), txt_modelo.value, capacidad):
            mostrar_snack("¡Camión registrado exitosamente!")
            txt_placa.value = ""
            txt_modelo.value = ""
            txt_capacidad.value = "0.0"
            txt_placa.update()
            txt_modelo.update()
            txt_capacidad.update()
            actualizar_tabla()
        else:
            mostrar_snack("Error: Esa placa ya se encuentra registrada.")

    def btn_eliminar_click(e):
        camion_id = e.control.data
        eliminar_camion(camion_id)
        mostrar_snack("Camión eliminado del sistema.")
        actualizar_tabla()

    def mostrar_snack(texto):
        page.snack_bar = ft.SnackBar(ft.Text(texto))
        page.snack_bar.open = True
        page.update()

    # Carga inicial de datos
    actualizar_tabla()

    return ft.Column([
        ft.Text("Administración de Camiones", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Registra y gestiona las unidades de transporte de la flota.", size=14, color="bluegrey200"),
        ft.Divider(height=20),
        
        # Formulario de entrada
        ft.Row([
            txt_placa,
            txt_modelo,
            txt_capacidad,
            ft.ElevatedButton(
                "Guardar Camión",
                icon=ft.icons.ADD,
                style=ft.ButtonStyle(bgcolor="green700", color="white"),
                on_click=btn_guardar_click
            )
        ], wrap=True, spacing=15),
        
        ft.Divider(height=30),
        ft.Text("Flota Registrada", size=18, weight=ft.FontWeight.BOLD),
        
        # Contenedor con scroll por si hay muchos datos
        ft.Container(
            content=ft.ListView([tabla_datos], expand=True),
            expand=True,
            margin=ft.margin.only(top=10)
        )
    ], expand=True)