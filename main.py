import flet as ft
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from database import init_db
from views.login import LoginView
from views.register import RegisterView
from views.dashboard import DashboardView
from views.cantidad_residuos import CantidadResiduosView

# Módulos secundarios (por si no existen todavía)
try: from views.camiones import CamionesView
except ImportError: CamionesView = lambda page: ft.Container(ft.Text("Módulo Camiones"))

try: from views.personal import PersonalView
except ImportError: PersonalView = lambda page: ft.Container(ft.Text("Módulo Personal"))

try: from views.reporte import ReporteView
except ImportError: ReporteView = lambda page: ft.Container(ft.Text("Módulo Reportes"))

try: from views.setting import SettingView
except ImportError: SettingView = lambda page: ft.Container(ft.Text("Módulo Configuración"))


def main(page: ft.Page):
    page.title = "Sistema de Gestión de Residuos"
    page.theme_mode = ft.ThemeMode.DARK
    init_db()

    if page.session.get("autenticado") is None:
        page.session.set("autenticado", False)

    def cambiar_ruta(index):
        rutas = ["/dashboard", "/camiones", "/personal", "/residuos", "/reporte", "/setting"]
        page.go(rutas[index])

    def salir_sistema(e):
        page.session.set("autenticado", False)
        page.go("/login")

    # =========================================================================
    # 🏗️ PLANTILLA MAESTRA CON DESEMPAQUETADO ANTICRASH
    # =========================================================================
    def CrearLayoutMenu(contenido_interno, boton_activo_index):
        # 🛡️ CLAVE: Si la vista viene envuelta en un ft.View por error, extraemos sus controles
        if isinstance(contenido_interno, ft.View):
            contenido_limpio = ft.Column(contenido_interno.controls, expand=True, scroll=ft.ScrollMode.AUTO)
        else:
            contenido_limpio = contenido_interno

        return ft.View(
            route=page.route,
            controls=[
                # Banner Superior Verde (Ancho completo)
                ft.Container(
                    content=ft.Row([
                        ft.Text("EcoGestión - Panel de Control", size=20, weight="bold", color="white"),
                        ft.IconButton(icon=ft.icons.EXIT_TO_APP, icon_color="white", on_click=salir_sistema)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=ft.colors.GREEN_700,
                    padding=15
                ),
                # Cuerpo Inferior: Menú Lateral + Contenido Limpio
                ft.Row([
                    ft.NavigationRail(
                        selected_index=boton_activo_index,
                        label_type=ft.NavigationRailLabelType.ALL,
                        min_width=100,
                        group_alignment=-0.9,
                        destinations=[
                            ft.NavigationRailDestination(icon=ft.icons.HOME_ROUNDED, selected_icon=ft.icons.HOME, label="Inicio"),
                            ft.NavigationRailDestination(icon=ft.icons.LOCAL_SHIPPING_OUTLINED, selected_icon=ft.icons.LOCAL_SHIPPING, label="Camiones"),
                            ft.NavigationRailDestination(icon=ft.icons.PEOPLE_OUTLINED, selected_icon=ft.icons.PEOPLE, label="Personal"),
                            ft.NavigationRailDestination(icon=ft.icons.BAR_CHART_OUTLINED, selected_icon=ft.icons.BAR_CHART, label="Residuos"),
                            ft.NavigationRailDestination(icon=ft.icons.ASSIGNMENT_OUTLINED, selected_icon=ft.icons.ASSIGNMENT, label="Reportes"),
                            ft.NavigationRailDestination(icon=ft.icons.SETTINGS_OUTLINED, selected_icon=ft.icons.SETTINGS, label="Configurar"),
                        ],
                        on_change=lambda e: cambiar_ruta(e.control.selected_index)
                    ),
                    ft.VerticalDivider(width=1),
                    ft.Container(content=contenido_limpio, expand=True, padding=20)
                ], expand=True)
            ],
            padding=0
        )

    # =========================================================================
    # 🔄 GESTIONADOR DE RUTAS NATIVO
    # =========================================================================
    def route_change(e):
        # 🛡️ EXCEPCIÓN DE SEGURIDAD CRÍTICA:
        # Si el usuario NO está autenticado, solo puede visitar "/login" o "/register"
        if not page.session.get("autenticado") and page.route not in ["/login", "/register"]:
            page.route = "/login"

        page.views.clear()

        # 🔐 Vista Login (Acceso público)
        if page.route == "/login":
            vista_login = LoginView(page)
            if isinstance(vista_login, ft.View):
                page.views.append(vista_login)
            else:
                page.views.append(ft.View(route="/login", controls=[vista_login]))
        
        # 📝 Vista Registro (Acceso público) <--- REVISA QUE ESTO ESTÉ EXACTAMENTE ASÍ
        elif page.route == "/register":
            vista_registro = RegisterView(page)
            if isinstance(vista_registro, ft.View):
                page.views.append(vista_registro)
            else:
                page.views.append(ft.View(route="/register", controls=[vista_registro]))
        
        # 📊 Módulos Privados con Menú (Requieren autenticación previa)
        elif page.route == "/dashboard":
            page.views.append(CrearLayoutMenu(DashboardView(page), 0))
            
        elif page.route == "/camiones":
            page.views.append(CrearLayoutMenu(CamionesView(page), 1))
            
        elif page.route == "/personal":
            page.views.append(CrearLayoutMenu(PersonalView(page), 2))
            
        elif page.route == "/residuos":
            page.views.append(CrearLayoutMenu(CantidadResiduosView(page), 3))
            
        elif page.route == "/reporte":
            page.views.append(CrearLayoutMenu(ReporteView(page), 4))
            
        elif page.route == "/setting":
            page.views.append(CrearLayoutMenu(SettingView(page), 5))

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")

ft.app(target=main)