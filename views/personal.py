import flet as ft
from database import crear_personal, obtener_personal, eliminar_personal

def PersonalView(page: ft.Page):
    txt_cedula = ft.TextField(label="Cédula de Identidad", width=180)
    txt_nombre = ft.TextField(label="Nombre Completo", width=250)
    txt_telefono = ft.TextField(label="Teléfono de Contacto", width=180)
    
    drop_rol = ft.Dropdown(
        label="Rol / Cargo",
        width=180,
        options=[
            ft.dropdown.Option("Chofer"),
            ft.dropdown.Option("Operador"),
            ft.dropdown.Option("Supervisor"),
        ],
        value="Chofer"
    )

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Cédula")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Rol")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def actualizar_tabla():
        tabla_datos.rows.clear()
        for p in obtener_personal():
            p_id, cedula, nombre, rol, telefono = p
            tabla_datos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(cedula)),
                        ft.DataCell(ft.Text(nombre)),
                        ft.DataCell(ft.Text(rol)),
                        ft.DataCell(ft.Text(telefono)),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINE,
                                icon_color="red400",
                                data=p_id,
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
        if not txt_cedula.value or not txt_nombre.value or not txt_telefono.value:
            mostrar_snack("Por favor, rellene todos los campos.")
            return

        if crear_personal(txt_cedula.value, txt_nombre.value, drop_rol.value, txt_telefono.value):
            mostrar_snack("Personal registrado con éxito.")
            txt_cedula.value = ""
            txt_nombre.value = ""
            txt_telefono.value = ""
            txt_cedula.update()
            txt_nombre.update()
            txt_telefono.update()
            actualizar_tabla()
        else:
            mostrar_snack("Error: Esta cédula ya está registrada.")

    def btn_eliminar_click(e):
        personal_id = e.control.data
        eliminar_personal(personal_id)
        mostrar_snack("Registro de personal eliminado.")
        actualizar_tabla()

    def mostrar_snack(texto):
        page.snack_bar = ft.SnackBar(ft.Text(texto))
        page.snack_bar.open = True
        page.update()

    actualizar_tabla()

    return ft.Column([
        ft.Text("Control de Personal", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Gestión de choferes, recolectores y personal operativo.", size=14, color="bluegrey200"),
        ft.Divider(height=20),
        
        ft.Row([
            txt_cedula,
            txt_nombre,
            drop_rol,
            txt_telefono,
            ft.ElevatedButton(
                "Registrar",
                icon=ft.icons.PERSON_ADD,
                style=ft.ButtonStyle(bgcolor="green700", color="white"),
                on_click=btn_guardar_click
            )
        ], wrap=True, spacing=15),
        
        ft.Divider(height=30),
        ft.Text("Nómina de Operadores", size=18, weight=ft.FontWeight.BOLD),
        
        ft.Container(
            content=ft.ListView([tabla_datos], expand=True),
            expand=True
        )
    ], expand=True)