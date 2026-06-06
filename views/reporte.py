import flet as ft
import os
import webbrowser
from database import obtener_estadisticas_por_tipo, obtener_reporte_detallado

def ReporteView(page: ft.Page):
    
    # 📊 1. CONSTRUCCIÓN DEL GRÁFICO DE ESTADÍSTICAS (MEJORADO CON EJES NUMÉRICOS)
    def generar_grafico():
        datos_stats = obtener_estadisticas_por_tipo()
        rod_groups = []
        colores = ["green", "blue", "orange", "amber", "purple", "grey"]
        
        labels_eje_x = []
        
        for i, (tipo, total) in enumerate(datos_stats):
            color = colores[i % len(colores)]
            rod_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=total,
                            color=color,
                            width=30,
                            tooltip=f"{tipo}: {total:.2f} Ton",
                            border_radius=5
                        )
                    ]
                )
            )
            # Agregar etiquetas inferiores cortas para el identificador del eje X
            labels_eje_x.append(
                ft.ChartAxisLabel(
                    value=i, 
                    label=ft.Container(
                        content=ft.Text(tipo[:5] + ".", size=11, weight=ft.FontWeight.BOLD),
                        margin=ft.margin.only(top=5)
                    )
                )
            )
            
        return ft.BarChart(
            bar_groups=rod_groups,
            border=ft.border.all(1, "grey700"),
            vertical_grid_lines=ft.ChartGridLines(interval=10, color="grey800", width=1),
            horizontal_grid_lines=ft.ChartGridLines(interval=10, color="grey800", width=1),
            # Eje Y: Visualiza números del 0 al 100 de diez en diez
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=v, label=ft.Text(f"{v}", size=11)) 
                    for v in range(0, 101, 10)
                ],
                labels_size=30,
            ),
            # Eje X: Visualiza los nombres cortos de los tipos debajo de sus barras
            bottom_axis=ft.ChartAxis(
                labels=labels_eje_x,
                labels_size=25,
            ),
            min_y=0,
            max_y=100,
            expand=True
        )

    # 📋 2. LEYENDA DEL GRÁFICO (Métricas Relativas)
    def generar_leyenda():
        datos_stats = obtener_estadisticas_por_tipo()
        colores = ["green", "blue", "orange", "amber", "purple", "grey"]
        items = []
        
        if not datos_stats:
            return ft.Text("No hay datos registrados aún.", size=13, color="grey500")
            
        for i, (tipo, total) in enumerate(datos_stats):
            color = colores[i % len(colores)]
            items.append(
                ft.Row([
                    ft.Container(width=12, height=12, bgcolor=color, border_radius=3),
                    ft.Text(f"{tipo} ({total:.2f} Ton)", size=12)
                ], spacing=8)
            )
        return ft.Column(items, spacing=5, scroll=ft.ScrollMode.AUTO)

    # 🖨️ 3. FUNCIÓN EXPORTAR A PDF / ASISTENTE DE IMPRESIÓN
    def imprimir_pdf_click(e):
        historial = obtener_reporte_detallado()
        
        filas_html = ""
        for r in historial:
            r_id, fecha, tipo, peso, placa, modelo = r
            filas_html += f"""
            <tr>
                <td>{r_id}</td>
                <td>{fecha}</td>
                <td>{tipo}</td>
                <td>{peso:.2f} Ton</td>
                <td>{placa if placa else 'N/A'} ({modelo if modelo else 'Sin modelo'})</td>
            </tr>
            """
            
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Reporte de Gestión de Residuos</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; color: #333; }}
                .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #2e7d32; padding-bottom: 10px; }}
                .logo-title {{ display: flex; align-items: center; }}
                .title {{ font-size: 24px; font-weight: bold; color: #2e7d32; margin-left: 10px; }}
                .subtitle {{ margin-top: 20px; font-weight: bold; font-size: 16px; }}
                .info {{ color: #666; font-size: 12px; margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #e8f5e9; color: #2e7d32; font-weight: bold; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                @media print {{
                    button {{ display: none; }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo-title">
                    <span style="font-size: 30px;">♻️</span>
                    <span class="title">ECOGESTIÓN - REPORTES GENERALES</span>
                </div>
            </div>
            <div class="subtitle">Balance Histórico de Disposición de Desechos</div>
            <div class="info">Documento oficial generado de forma automática por la suite del sistema.</div>
            
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Fecha</th>
                        <th>Clasificación</th>
                        <th>Peso Recolectado</th>
                        <th>Unidad / Placa</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_html}
                </tbody>
            </table>
            
            <script>
                window.onload = function() {{ window.print(); }}
            </script>
        </body>
        </html>
        """
        
        file_path = os.path.abspath("reporte_temp.html")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        webbrowser.open(f"file://{file_path}")
        
        page.snack_bar = ft.SnackBar(ft.Text("Reporte enviado al navegador. Guarde el documento como PDF."))
        page.snack_bar.open = True
        page.update()

    # 🗂️ INTERFAZ DE USUARIO DEL MÓDULO DE REPORTES (OPTIMIZADA)
    return ft.Column([
        ft.Row([
            ft.Column([
                ft.Text("Estadísticas y Reportes", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Métricas consolidadas del tonelaje total descargado.", size=14, color="bluegrey200"),
            ]),
            ft.ElevatedButton(
                "Exportar a PDF / Imprimir",
                icon=ft.icons.PICTURE_AS_PDF,
                style=ft.ButtonStyle(bgcolor="red700", color="white"),
                on_click=imprimir_pdf_click
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        
        ft.Divider(height=20),
        
        ft.Text("Distribución de Residuos por Categoría (Toneladas)", size=18, weight=ft.FontWeight.BOLD),
        ft.Row([
            # Contenedor del gráfico de barras analítico con padding y escala ajustados
            ft.Container(
                content=generar_grafico(),
                bgcolor="surfaceVariant",
                padding=ft.padding.only(left=15, top=25, right=25, bottom=15),
                border_radius=10,
                height=400,
                expand=2
            ),
            # Contenedor de la leyenda explicativa con la misma altura para perfecta simetría
            ft.Container(
                content=ft.Column([
                    ft.Text("Métricas Relativas", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=10),
                    ft.Container(content=generar_leyenda(), expand=True)
                ]),
                bgcolor="surfaceVariant",
                padding=20,
                border_radius=10,
                height=400,
                expand=1
            )
        ], spacing=15, alignment=ft.MainAxisAlignment.START)
    ], expand=True, spacing=15)