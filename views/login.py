import flet as ft
from database import verificar_usuario  

def LoginView(page: ft.Page):
    
    usuario_input = ft.TextField(
        label="Correo Electrónico", 
        width=300,
        prefix_icon=ft.icons.EMAIL_ROUNDED,
         
    )
    contrasena_input = ft.TextField(
        label="Contraseña", 
        password=True, 
        can_reveal_password=True, 
        width=300,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        
    )
    
    mensaje_error = ft.Text("", color=ft.colors.RED_400, size=14, weight="bold")

    def login_click(e):
        usuario_input.error_text = None
        contrasena_input.error_text = None
        mensaje_error.value = ""
        
        if not usuario_input.value:
            usuario_input.error_text = "El correo es obligatorio"
            page.update()
            return
            
        if not contrasena_input.value:
            contrasena_input.error_text = "La contraseña es obligatoria"
            page.update()
            return

        usuario_found = verificar_usuario(usuario_input.value, contrasena_input.value)

        if usuario_found is not None:
            page.session.set("autenticado", True)
            page.session.set("usuario_nombre", usuario_found[0]) 
            page.go("/dashboard")
        else:
            mensaje_error.value = "Correo o contraseña incorrectos"
            page.update()

    boton_entrar = ft.ElevatedButton(
        text="Iniciar Sesión",
        on_click=login_click,
        width=300,
        style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_700, color=ft.colors.WHITE)
    )

    # 🆕 BOTÓN CRÍTICO: Redirige al módulo de registro que acabas de pulir
    boton_ir_registro = ft.TextButton(
        text="¿No tienes usuario? Regístrate aquí",
        on_click=lambda e: page.go("/register")
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Sistema de Gestión de Residuos Sólidos", size=35, weight="bold", color=ft.colors.GREEN, text_align="center"),
                ft.Text("EcoGestión2026", size=32, weight="bold", color=ft.colors.GREEN_700),
                ft.Text("Inicia sesión para acceder al sistema", size=14, color="bluegrey200"),
                ft.Divider(height=20, color="transparent"),
                usuario_input,
                contrasena_input,
                mensaje_error,
                ft.Divider(height=10, color="transparent"),
                boton_entrar,
                boton_ir_registro  # Enlace visual activo
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )
#Sistema desarrollado por Ing Anderson Rondon Laya, desarrollador con 5 años de experiencia,
#diseñando soluciones tecnologicas para Empresas, Pymes, negocios o uso personal 