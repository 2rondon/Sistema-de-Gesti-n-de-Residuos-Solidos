import flet as ft
from database import obtener_configuracion, actualizar_configuracion

def SettingView(page: ft.Page):
    config = obtener_configuracion()
    
    # Inputs basados en los datos guardados
    txt_limite = ft.TextField(
        label="Límite Crítico de Alerta (Toneladas)", 
        width=250, 
        value=config.get("limite_alerta_ton", "10.0")
    )
    
    switch_tema = ft.Switch(
        label="Modo Oscuro (Fondo de Interfaz)", 
        value=True if config.get("modo_oscuro", "True") == "True" else False
    )

    def btn_guardar_ajustes(e):
        try:
            limite = float(txt_limite.value)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("El límite debe ser un valor numérico."))
            page.snack_bar.open = True
            page.update()
            return

        # Guardar en SQLite
        actualizar_configuracion("limite_alerta_ton", str(limite))
        actualizar_configuracion("modo_oscuro", str(switch_tema.value))
        
        # Aplicar cambio de tema en tiempo real a la ventana actual
        page.theme_mode = ft.ThemeMode.DARK if switch_tema.value else ft.ThemeMode.LIGHT
        
        page.snack_bar = ft.SnackBar(ft.Text("Configuraciones guardadas y aplicadas."))
        page.snack_bar.open = True
        page.update()

    return ft.Column([
        ft.Text("Ajustes del Sistema", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Modifica los parámetros operacionales generales de EcoGestión.", size=14, color="bluegrey200"),
        ft.Divider(height=20),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Preferencias Visuales", size=18, weight=ft.FontWeight.BOLD),
                switch_tema,
                ft.Divider(height=15),
                ft.Text("Parámetros de Operación", size=18, weight=ft.FontWeight.BOLD),
                txt_limite,
                ft.Divider(height=20),
                ft.ElevatedButton(
                    "Guardar Configuración",
                    icon=ft.icons.SAVE,
                    style=ft.ButtonStyle(bgcolor="green700", color="white"),
                    on_click=btn_guardar_ajustes
                )
            ], spacing=15),
            padding=10
        )
    ], expand=True)