import flet as ft
from database import registrar_usuario  # 🗄️ Importación de tu función real

def RegisterView(page: ft.Page):
    # Inputs del formulario de registro con iconos nativos estandarizados
    txt_name = ft.TextField(label="Nombre Completo", width=300, prefix_icon=ft.icons.PERSON)
    txt_email = ft.TextField(label="Correo Electrónico", width=300, prefix_icon=ft.icons.EMAIL)
    txt_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300, prefix_icon=ft.icons.LOCK)
    
    def register_click(e):
        # Validación de campos vacíos
        if txt_name.value.strip() == "" or txt_email.value.strip() == "" or txt_pass.value.strip() == "":
            mostrar_snack("Por favor, llena todos los campos.")
            return
        
        # 💾 LOGICA REAL: Guardado directo en la base de datos sqlite3
        # 'registrar_usuario' retorna True si tuvo éxito o False si hay duplicados (IntegrityError)
        guardado_exitoso = registrar_usuario(txt_name.value, txt_email.value, txt_pass.value)
        
        if guardado_exitoso:
            mostrar_snack("¡Usuario registrado con éxito!")
            # Redireccionamos al login usando el enrutador nativo
            page.go("/login")
        else:
            mostrar_snack("Error: Este Correo Electrónico ya está registrado.")

    def mostrar_snack(texto):
        page.snack_bar = ft.SnackBar(ft.Text(texto))
        page.snack_bar.open = True
        page.update()

    return ft.View(
        route="/register",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.icons.PERSON_ADD_ROUNDED, size=80, color="green400"),
                        ft.Text("Crear Cuenta", size=28, weight=ft.FontWeight.BOLD),
                        ft.Text("Regístrate en el Sistema de Residuos", size=14, color="bluegrey200"),
                        ft.Divider(height=10, color="transparent"),
                        txt_name,
                        txt_email,
                        txt_pass,
                        ft.Divider(height=10, color="transparent"),
                        ft.ElevatedButton(
                            "Registrarse", 
                            width=300, 
                            on_click=register_click, 
                            style=ft.ButtonStyle(bgcolor="green700", color="white")
                        ),
                        ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=lambda _: page.go("/login"))
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )