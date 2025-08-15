import os
import time
import psutil
import tkinter as tk
from tkinter import messagebox
from playwright.sync_api import sync_playwright
import subprocess

# Caminhos
BASE_DIR = os.getcwd()
CHROMIUM_PATH = os.path.join(BASE_DIR, "chrome", "browser.exe")   # requer chromium
USER_DATA_DIR = os.path.join(BASE_DIR, "user_data")               # pasta onde fica o perfil

# URLs
LOGIN_URL = "https://accounts.google.com/"
ACTIVITY_URL = "https://myactivity.google.com/page?hl=en&utm_medium=web&utm_source=youtube&page=youtube_comments"

# Seletor para botões de deletar
SEL_DELETE = 'button[aria-label^="Delete activity item"]'

def fechar_chromium():
    """Fecha apenas o Chromium renomeado para browser.exe."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and proc.info['name'].lower() == "browser.exe":
            try:
                proc.kill()
            except Exception:
                pass
            
def abrir_login():
    """Abre o Chromium externo para login manual."""
    if not os.path.exists(CHROMIUM_PATH):
        messagebox.showerror("Erro", f"Chromium não encontrado em:\n{CHROMIUM_PATH}")
        return
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    subprocess.Popen([
        CHROMIUM_PATH,
        f"--user-data-dir={USER_DATA_DIR}",
        "--start-maximized",
        LOGIN_URL
    ])

def click_all_visible(page, pause=0.25) -> int:
    """Clica em todos os botões Delete activity item visíveis."""
    deleted = 0
    while page.locator(SEL_DELETE).count() > 0:
        for btn in page.locator(SEL_DELETE).all():
            try:
                btn.scroll_into_view_if_needed()
                btn.click(timeout=3000)
                time.sleep(pause)
                deleted += 1
            except:
                continue
        time.sleep(0.3)
    return deleted

def scroll_for_more(page, times=8, dy=2400, pause=0.8):
    """Rola a página para carregar mais itens."""
    for _ in range(times):
        page.mouse.wheel(0, dy)
        time.sleep(pause)

def reached_end(page) -> bool:
    """Verifica se chegou ao fim da lista."""
    markers = [
        'text=No activity',
        'text=No more activity',
        'text=You don’t have any activity',
        "text=You don't have any activity",
    ]
    return any(page.locator(m).first.is_visible() for m in markers)

def deletar_atividade():
    """Fecha Chromium e executa o processo de deleção com Playwright."""
    if not os.path.exists(CHROMIUM_PATH):
        messagebox.showerror("Erro", f"Chromium não encontrado em:\n{CHROMIUM_PATH}")
        return
    fechar_chromium()
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            executable_path=CHROMIUM_PATH,
            args=["--start-maximized"]
        )
        page = ctx.new_page()
        page.set_default_timeout(60000)
        page.goto(ACTIVITY_URL, wait_until="domcontentloaded", timeout=60000)

        total = 0
        dry_rounds = 0
        while True:
            deleted_now = click_all_visible(page, pause=0.25)
            total += deleted_now
            if deleted_now == 0:
                dry_rounds += 1
                scroll_for_more(page, times=10)
                deleted_now = click_all_visible(page, pause=0.25)
                total += deleted_now
                if deleted_now == 0 and (reached_end(page) or dry_rounds >= 3):
                    break
            else:
                dry_rounds = 0

        messagebox.showinfo("Finalizado", f"Comentários deletados: {total}")

# Interface gráfica
root = tk.Tk()
root.title("YouTube Activity Deleter")
root.geometry("800x600")
icon_path = os.path.join(os.path.dirname(__file__), "favicon.ico") #comente se preferir
root.iconbitmap(icon_path)                                          #comente se preferir
root.resizable(False, False)

frame_botoes = tk.Frame(root)
frame_botoes.pack(side="bottom", pady=20)

btn_login = tk.Button(frame_botoes, text="Login", command=abrir_login,
                      width=20, height=2, bg="#4CAF50", fg="white")
btn_login.pack(side="left", padx=20)

btn_delete = tk.Button(frame_botoes, text="Deletar atividade", command=deletar_atividade,
                       width=20, height=2, bg="#F44336", fg="white")
btn_delete.pack(side="left", padx=20)

root.mainloop()
