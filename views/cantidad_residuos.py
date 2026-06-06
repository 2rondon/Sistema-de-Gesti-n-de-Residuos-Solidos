import flet as ft
from database import (
    obtener_reporte_detallado, 
    registrar_pesaje_residuo,
    actualizar_residuo, 
    eliminar_residuo,
    obtener_camiones
)

def CantidadResiduosView(page: ft.Page):
    # Usamos una lista de un elemento como celda de memoria para el ID que estamos editando
    id_editando = [None] 

    # =========================================================================
    # ⚙️ COMPONENTES DEL FORMULARIO SUPERIOR
    # =========================================================================
    dropdown_clasificacion = ft.Dropdown(
        label="Clasificación de Residuo",
        options=[
            ft.dropdown.Option("Desechos Generales"),
            ft.dropdown.Option("Orgánico"),
            ft.dropdown.Option("Metal"),
            ft.dropdown.Option("Plástico"),
            ft.dropdown.Option("Vidrio/Papel"),
        ],
        width=230,
        value="Desechos Generales"
    )
    
    txt_peso = ft.TextField(
        label="Peso Despachado (Ton)", 
        value="0.0", 
        width=150,
        text_align=ft.TextAlign.RIGHT
    )
    
    dropdown_camion = ft.Dropdown(
        label="Camión Transportador", 
        width=180
    )
    
    # Poblamos el dropdown de camiones con las placas activas de la BD
    try:
        camiones_bd = obtener_camiones()
        dropdown_camion.options = [ft.dropdown.Option(c[1]) for c in camiones_bd]
        if dropdown_camion.options:
            dropdown_camion.value = dropdown_camion.options[0].key
    except Exception:
        dropdown_camion.options = [ft.dropdown.Option("ABX4582")]
        dropdown_camion.value = "ABX4582"

    # Botón Principal de Acción (Registrar / Guardar)
    btn_registrar = ft.ElevatedButton(
        text="Registrar Pesaje",
        icon=ft.icons.SCALE,
        style=ft.ButtonStyle(bgcolor="green700", color="white"),
    )

    # =========================================================================
    # 📋 ESTRUCTURA DE LA TABLA DE HISTORIAL
    # =========================================================================
    tabla_historial = ft.DataTable(
        heading_row_color="surfaceVariant",
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Clasificación", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Peso", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Camión", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", weight=ft.FontWeight.BOLD)), # 🛠️ Columna de Control
        ],
        rows=[]
    )

    # =========================================================================
    # 🔄 LÓGICA DE CARGA Y ACTUALIZACIÓN EN TIEMPO REAL
    # =========================================================================
    def cargar_historial():
        historial = obtener_reporte_detallado()
        tabla_historial.rows.clear()
        
        for r in historial:
            # Desestructuramos la tupla de la BD
            r_id, fecha, tipo, peso, placa, modelo = r
            
            # Forzamos la captura de valores actuales para evitar el problema de clausura en bucles (closures)
            def crear_evento_eliminar(id_borrar=r_id):
                return lambda e: click_eliminar(id_borrar)

            def crear_evento_editar(id_mod=r_id, t=tipo, p=peso, c=placa):
                return lambda e: click_editar(id_mod, t, p, c)

            # Insertamos la fila estructurada
            tabla_historial.rows.append(
                ft.DataRow([
                    ft.DataCell(ft.Text(str(r_id))),
                    ft.DataCell(ft.Text(fecha)),
                    ft.DataCell(ft.Text(tipo)),
                    ft.DataCell(ft.Text(f"{peso:.1f} Ton")),
                    ft.DataCell(ft.Text(placa if placa else "N/A")),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.EDIT_OUTLINED,
                                icon_color="orange500",
                                tooltip="Editar Pesaje",
                                on_click=crear_evento_editar()
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINED,
                                icon_color="red500",
                                tooltip="Eliminar Pesaje",
                                on_click=crear_evento_eliminar()
                            ),
                        ], spacing=0)
                    )
                ])
            )
        page.update()

    # Accionamiento del botón de borrado
    def click_eliminar(id_borrar):
        eliminar_residuo(id_borrar)
        cargar_historial()
        
        # Si borramos el registro que estábamos editando, reseteamos el formulario
        if id_editando[0] == id_borrar:
            cancelar_edicion()
            
        page.snack_bar = ft.SnackBar(ft.Text(f"Registro #{id_borrar} eliminado correctamente."), bgcolor="red700")
        page.snack_bar.open = True
        page.update()

    # Accionamiento del botón de edición (Sube los datos al formulario)
    def click_editar(id_mod, tipo, peso, placa):
        id_editando[0] = id_mod
        dropdown_clasificacion.value = tipo
        txt_peso.value = str(peso)
        dropdown_camion.value = placa if placa else ""
        
        # Cambiamos visualmente el botón de acción
        btn_registrar.text = "Guardar Cambios"
        btn_registrar.icon = ft.icons.SAVE
        btn_registrar.style = ft.ButtonStyle(bgcolor="orange800", color="white")
        page.update()

    def cancelar_edicion():
        id_editando[0] = None
        dropdown_clasificacion.value = "Desechos Generales"
        txt_peso.value = "0.0"
        btn_registrar.text = "Registrar Pesaje"
        btn_registrar.icon = ft.icons.SCALE
        btn_registrar.style = ft.ButtonStyle(bgcolor="green700", color="white")

    # Manejador del botón verde/naranja del formulario
    def ejecutar_accion_pesaje(e):
        # Validamos que el peso sea un número válido
        try:
            peso_validado = float(txt_peso.value)
            if peso_validado < 0: raise ValueError
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, ingrese un número de peso válido (mayor o igual a 0)."), bgcolor="amber800")
            page.snack_bar.open = True
            page.update()
            return

        if id_editando[0] is None:
            # Modo inserción normal
            registrar_pesaje_residuo(
                dropdown_clasificacion.value,
                peso_validado,
                dropdown_camion.value
            )
            mensaje = "Nuevo pesaje registrado con éxito."
        else:
            # Modo edición (Sobrescribe usando el ID de control)
            actualizar_residuo(
                id_editando[0],
                dropdown_clasificacion.value,
                peso_validado,
                dropdown_camion.value
            )
            mensaje = f"Registro #{id_editando[0]} actualizado correctamente."
            cancelar_edicion()

        # Limpiamos el campo de texto y refrescamos la grilla
        txt_peso.value = "0.0"
        cargar_historial()
        
        page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor="green700")
        page.snack_bar.open = True
        page.update()

    # Asignamos el evento al botón
    btn_registrar.on_click = ejecutar_accion_pesaje

    # Primera carga de datos al instanciar la vista
    cargar_historial()

    # =========================================================================
    # 🎨 MAQUETADO VISUAL COMPLETO (INTERFAZ DE USUARIO)
    # =========================================================================
    return ft.Column([
        # Fila de Títulos principales del módulo
        ft.Column([
            ft.Text("Ingreso y Control de Residuos", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Báscula de pesaje y clasificación del volumen recolectado.", size=14, color="bluegrey200"),
        ]),
        ft.Divider(height=10),
        
        # Bloque horizontal con los inputs de captura de datos
        ft.Row([
            dropdown_clasificacion,
            txt_peso,
            dropdown_camion,
            ft.Container(content=btn_registrar, margin=ft.margin.only(top=15))
        ], alignment=ft.MainAxisAlignment.START, spacing=15),
        
        ft.Divider(height=20),
        
        # Historial y su correspondiente grilla de datos modificable
        ft.Text("Historial de Descargas Recientes", size=18, weight=ft.FontWeight.BOLD),
        ft.Container(
            content=ft.Column([
                tabla_historial
            ], scroll=ft.ScrollMode.AUTO),
            expand=True
        )
    ], expand=True, spacing=15)