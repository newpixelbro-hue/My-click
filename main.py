import flet as ft

def main(page: ft.Page):
    page.title = "Pixel Clicker"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    score = 0
    score_text = ft.Text(value="Очки: 0", size=40, weight=ft.FontWeight.BOLD, color="green")

    def button_click(e):
        nonlocal score
        score += 1
        score_text.value = f"Очки: {score}"
        page.update()

    click_button = ft.ElevatedButton(
        text="ТАПАЙ МЕНЯ! 🪙",
        on_click=button_click,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            padding=30,
            text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
        )
    )

    page.add(
        ft.Text("Моё первое приложение! 🚀", size=24),
        score_text,
        ft.Container(height=20),
        click_button
    )

ft.app(target=main)
