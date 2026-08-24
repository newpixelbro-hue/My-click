import flet as ft
import time
import threading
import os

def main(page: ft.Page):
    page.title = "Pixel Clicker: Evolution"
    page.icon = "icongame.png"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- БРОНЕБОЙНОЕ СОХРАНЕНИЕ ЧЕРЕЗ ФАЙЛ (ЗАМЕНА CLIENT_STORAGE) ---
    save_file = "save.txt"

    def save_data(b, cp, pi, e, lb):
        try:
            with open(save_file, "w") as f:
                f.write(f"{b},{cp},{pi},{e},{lb}")
        except:
            pass

    def load_data():
        if os.path.exists(save_file):
            try:
                with open(save_file, "r") as f:
                    data = f.read().split(",")
                    return int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4])
            except:
                return 0, 1, 0, 1000, 0
        return 0, 1, 0, 1000, 0

    # Загружаем циферки из памяти
    balance, click_power, p_income, energy, last_bonus = load_data()
    max_energy = 1000

    multitap_cost = click_power * 150
    gpu_cost = (p_income + 1) * 200

    # --- ВИДЖЕТЫ ИНТЕРФЕЙСА (ОБЩИЕ) ---
    balance_text = ft.Text(value=f"🪙 {balance:,} MOНET", size=32, weight=ft.FontWeight.BOLD, color="amber")
    income_text = ft.Text(value=f"⚡ Прибыль в сек: +{p_income}", size=14, color="cyan", font_family="monospace")
    
    # --- ЭКРАН 1: ГЛАВНАЯ (ТАПАЛКА) ---
    rank_text = ft.Text(value="Ранг: Новичок с Пикселем", size=14, color="lightgreen", weight=ft.FontWeight.BOLD)
    energy_bar = ft.ProgressBar(value=energy/max_energy, width=300, color="green", bgcolor="#333333")
    energy_text = ft.Text(value=f"🔋 Энергия: {energy}/{max_energy}", size=12, color="green")

    def update_rank():
        if balance < 5000: rank_text.value = "Ранг: Новичок с Пикселем"
        elif balance < 50000: rank_text.value = "Ранг: Продвинутый Хакер 💻"
        else: rank_text.value = "Ранг: Крипто-Монарх 👑"

    def coin_tap(e):
        nonlocal balance, energy
        if energy >= click_power:
            balance += click_power
            energy -= click_power
            save_data(balance, click_power, p_income, energy, last_bonus)
            
            balance_text.value = f"🪙 {balance:,} MOНET"
            energy_bar.value = energy / max_energy
            energy_text.value = f"🔋 Энергия: {energy}/{max_energy}"
            update_rank()
            page.update()

    tap_button = ft.IconButton(
        icon=ft.Icons.MONETIZATION_ON,
        icon_size=100,
        icon_color="amber",
        on_click=coin_tap
    )

    tab_main = ft.Column([
        rank_text,
        ft.Container(height=10),
        tap_button,
        ft.Container(height=20),
        energy_text,
        energy_bar,
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)


    # --- ЭКРАН 2: МАГАЗИН (МАЙНИНГ) ---
    multitap_btn_text = ft.Text(f"Прокачать Клик (+1)\nЦена: {multitap_cost} 🪙", size=12, color="white")
    gpu_btn_text = ft.Text(f"Купить Процессор Tensor (+2/сек)\nЦена: {gpu_cost} 🪙", size=12, color="white")

    def buy_multitap(e):
        nonlocal balance, click_power, multitap_cost
        if balance >= multitap_cost:
            balance -= multitap_cost
            click_power += 1
            multitap_cost = click_power * 150
            save_data(balance, click_power, p_income, energy, last_bonus)
            
            balance_text.value = f"🪙 {balance:,} MOНET"
            multitap_btn_text.value = f"Прокачать Клик (+1)\nЦена: {multitap_cost} 🪙"
            page.update()

    def buy_gpu(e):
        nonlocal balance, p_income, gpu_cost
        if balance >= gpu_cost:
            balance -= gpu_cost
            p_income += 2
            gpu_cost = (p_income + 1) * 200
            save_data(balance, click_power, p_income, energy, last_bonus)
            
            balance_text.value = f"🪙 {balance:,} MOНET"
            income_text.value = f"⚡ Прибыль в сек: +{p_income}"
            gpu_btn_text.value = f"Купить Процессор Tensor (+2/сек)\nЦена: {gpu_cost} 🪙"
            page.update()

    tab_shop = ft.Column([
        ft.Text("🏢 УЛУЧШЕНИЯ И МАЙНИНГ", size=18, weight=ft.FontWeight.BOLD, color="cyan"),
        ft.Container(height=10),
        ft.ElevatedButton(content=multitap_btn_text, width=280, style=ft.ButtonStyle(padding=15), on_click=buy_multitap),
        ft.Container(height=10),
        ft.ElevatedButton(content=gpu_btn_text, width=280, style=ft.ButtonStyle(padding=15), on_click=buy_gpu),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)


    # --- ЭКРАН 3: КАЗИНО И БОНУСЫ ---
    casino_output = ft.Text("Испытай удачу в рулетке!", size=14, color="white", font_family="monospace")

    def claim_daily(e):
        nonlocal balance, last_bonus
        current_time = int(time.time())
        
        if current_time - last_bonus >= 86400:
            balance += 5000
            last_bonus = current_time
            save_data(balance, click_power, p_income, energy, last_bonus)
            balance_text.value = f"🪙 {balance:,} MOНET"
            casino_output.value = "🎁 Ежедневный бонус +5,000 монет получен!"
        else:
            left = 86400 - (current_time - last_bonus)
            casino_output.value = f"❌ Бонус еще не готов! Подождите {left // 3600} ч."
        page.update()

    def play_slots(e):
        nonlocal balance
        if balance >= 200:
            balance -= 200
            import random
            result = random.choice(["WIN", "LOSE", "JACKPOT"])
            
            if result == "WIN":
                balance += 500
                casino_output.value = "🎰 Слот-машина: ВЫИГРЫШ! +500 монет! 🎉"
            elif result == "JACKPOT":
                balance += 5000
                casino_output.value = "🔥 ДЖЕКПОТ!!! +5,000 монет! 🔥"
            else:
                casino_output.value = "😢 Слот-машина: Мимо... Попробуй еще раз (-200 🪙)"
                
            save_data(balance, click_power, p_income, energy, last_bonus)
            balance_text.value = f"🪙 {balance:,} MOНET"
        else:
            casino_output.value = "❌ Недостаточно монет для игры (нужно 200 🪙)"
        page.update()

    tab_casino = ft.Column([
        ft.Text("🎁 ПРИЗЫ И АЗАРТ", size=18, weight=ft.FontWeight.BOLD, color="purple"),
        ft.Container(height=10),
        ft.ElevatedButton("Забрать Ежедневный Бонус (+5000 🪙) 📅", width=280, on_click=claim_daily),
        ft.Container(height=10),
        ft.ElevatedButton("Крутить Слот-Машину (Ставка: 200 🪙) 🎰", width=280, on_click=play_slots),
        ft.Container(height=15),
        ft.Container(content=casino_output, bgcolor="#222222", padding=15, border_radius=8, width=280)
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)


    # --- СИСТЕМА НАВИГАЦИИ (UI ТАБЫ) ---
    main_container = ft.Container(content=tab_main, padding=15)

    def on_tab_change(e):
        if e.control.selected_index == 0:
            main_container.content = tab_main
        elif e.control.selected_index == 1:
            main_container.content = tab_shop
        elif e.control.selected_index == 2:
            main_container.content = tab_casino
        page.update()

    nav_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_tab_change,
        destinations=[
            ft.NavigationDestination(icon=ft.Icons.TOUCH_APP, label="Тапать"),
            ft.NavigationDestination(icon=ft.Icons.MONETIZATION_ON, label="Майнинг"),
            ft.NavigationDestination(icon=ft.Icons.CASINO, label="Бонусы"),
        ]
    )

    # --- ФОНОВЫЙ ПОТОК (ПАССИВНЫЙ ДОХОД И ЭНЕРГИЯ) ---
    def auto_worker():
        nonlocal balance, energy
        while True:
            time.sleep(1)
            if p_income > 0:
                balance += p_income
            if energy < max_energy:
                energy = min(max_energy, energy + 3)
            
            save_data(balance, click_power, p_income, energy, last_bonus)
            
            try:
                balance_text.value = f"🪙 {balance:,} MOНET"
                energy_bar.value = energy / max_energy
                energy_text.value = f"🔋 Энергия: {energy}/{max_energy}"
                page.update()
            except:
                break

    threading.Thread(target=auto_worker, daemon=True).start()

    # --- СБОРКА ИНТЕРФЕЙСА ---
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Container(content=balance_text, alignment=ft.alignment.center),
                income_text,
                ft.Divider(color="amber", height=2),
                ft.Container(content=main_container, height=320, alignment=ft.alignment.center),
                nav_bar
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
            bgcolor="#111111",
            border_radius=15,
            width=360
        )
    )

ft.app(target=main)
