import flet as ft
from database import obtener_metricas_dashboard

def DashboardView(page: ft.Page):
    
    # 📋 Consulta de las métricas directo de la base de datos
    camiones_activos, residuos_dia, residuos_mes, residuos_ano = obtener_metricas_dashboard()

    # 🎨 Molde base para fabricar tus tarjetas
    def crear_card(titulo: str, valor: str, icono: str, color_icono: str):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(name=icono, color=color_icono, size=32),
                    ft.Text(titulo, size=14, color="bluegrey200", weight=ft.FontWeight.W_500)
                ], spacing=10, alignment=ft.MainAxisAlignment.START),
                ft.Divider(height=10, color="transparent"),
                ft.Text(valor, size=24, weight=ft.FontWeight.BOLD, color="white")
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor="#1e293b", 
            padding=20,
            border_radius=12,
            width=200,
            height=130,
        )

    # 📊 Construcción de los bloques de información
    card_camiones = crear_card("Rutas Activas", f"{camiones_activos} Camiones", ft.icons.LOCAL_SHIPPING_ROUNDED, "green400")
    card_dia = crear_card("Residuos Hoy", f"{residuos_dia:.1f} Ton", ft.icons.TODAY_ROUNDED, "blue400")
    card_mes = crear_card("Residuos Mes", f"{residuos_mes:.1f} Ton", ft.icons.CALENDAR_MONTH_ROUNDED, "orange400")
    card_ano = crear_card("Residuos Año", f"{residuos_ano:.1f} Ton", ft.icons.ANALYTICS_ROUNDED, "purple400")

    # Retorna únicamente la columna de contenido interno del Dashboard
    return ft.Column([
        ft.Column([
            ft.Text("¡Bienvenido de vuelta, Administrador!", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Estado en tiempo real del Sistema de Gestión de Residuos", size=14, color="bluegrey200"),
        ]),
        ft.Divider(height=15, color="transparent"),
        
        # Fila horizontal con la colección de tarjetas métricas
        ft.Row([
            card_camiones,
            card_dia,
            card_mes,
            card_ano
        ], spacing=15, wrap=True, alignment=ft.MainAxisAlignment.START)
    ], spacing=10)