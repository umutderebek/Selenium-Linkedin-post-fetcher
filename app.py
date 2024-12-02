import json
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from io import BytesIO
import time

posts_data = []
unique_ids = set()

# LinkedIn verilerini çekme fonksiyonu
def fetch_posts(email, password):
    global posts_data, unique_ids


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        driver.find_element(By.ID, "username").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        # Değiştirilecek sayfa URL'si
        driver.get("https://www.linkedin.com/company/sicpa-assan/posts/?feedView=all")
        time.sleep(5)

        SCROLL_PAUSE_TIME = 3
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            posts = driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2')]")

            for post in posts:
                try:
                    unique_id = post.get_attribute("data-urn")
                    if unique_id in unique_ids:
                        continue

                    sender_name = post.find_element(By.XPATH, ".//span[contains(@class, 'update-components-actor__title')]").text
                    sender_info = post.find_element(By.XPATH, ".//span[contains(@class, 'update-components-actor__description')]").text
                    post_content = post.find_element(By.XPATH, ".//div[contains(@class, 'update-components-update-v2__commentary')]").text

                    try:
                        image_url = post.find_element(By.XPATH, ".//img[contains(@class, 'update-components-image__image')]").get_attribute("src")
                    except:
                        image_url = None

                    post_data = {
                        "id": unique_id,
                        "sender_name": sender_name,
                        "sender_info": sender_info,
                        "post_content": post_content,
                        "image_url": image_url,
                    }

                    posts_data.append(post_data)
                    unique_ids.add(unique_id)
                except:
                    pass

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    finally:
        driver.quit()

    display_table(posts_data)

# Tabloyu gösteren GUI
def display_table(posts):
    def refresh_table():
        """Tabloyu günceller ve güncel postları yeniden gösterir."""
        for widget in canvas_frame.winfo_children():
            widget.destroy()  # Mevcut satırları temizle
        for idx, post in enumerate(posts_data):  # Güncellenmiş posts_data'yı kullan
            row_frame = tk.Frame(canvas_frame, bg="white", relief="solid", bd=1)
            row_frame.pack(fill="x", pady=2)

            label_id = tk.Label(row_frame, text=post["id"], width=10, bg="white")
            label_id.pack(side="left", padx=5)

            label_name = tk.Label(row_frame, text=post["sender_name"], bg="white", anchor="w")
            label_name.pack(side="left", padx=5)

            label_content = tk.Label(row_frame, text=post["post_content"], bg="white", anchor="w", wraplength=400, justify="left")


            if post["image_url"]:
                try:
                    response = requests.get(post["image_url"])
                    img_data = Image.open(BytesIO(response.content))
                    img_data.thumbnail((50, 50))  # Küçük resim boyutu
                    img = ImageTk.PhotoImage(img_data)
                    label_image = tk.Label(row_frame, image=img, bg="white")
                    label_image.image = img
                    label_image.pack(side="left", padx=5)
                except:
                    tk.Label(row_frame, text="Yok", bg="white").pack(side="left", padx=5)
            else:
                tk.Label(row_frame, text="Yok", bg="white").pack(side="left", padx=5)

            btn_cancel = tk.Button(row_frame, text="Listeden Çıkart", command=lambda post_id=post["id"]: cancel_post(post_id), bg="red", fg="white")
            btn_cancel.pack(side="left", padx=5)

            btn_send = tk.Button(row_frame, text="Sisteme Gönder", command=lambda post_id=post["id"]: send_post(post_id), bg="green", fg="white")
            btn_send.pack(side="left", padx=5)

    def cancel_post(post_id):
        """Postu listeden çıkarır."""
        global posts_data
        # Postu posts_data listesinden çıkar
        posts_data = [post for post in posts_data if post["id"] != post_id]
        refresh_table()  # Tabloyu güncelle

    def send_post(post_id):
        """Postu sisteme gönderir ve listeden çıkarır."""
        global posts_data
        messagebox.showinfo("Başarılı", f"Post ID {post_id} sisteme gönderildi!")
        # Postu posts_data listesinden çıkar
        posts_data = [post for post in posts_data if post["id"] != post_id]
        refresh_table()  # Tabloyu güncelle

    root = tk.Tk()
    root.title("LinkedIn Post Yönetimi")
    root.geometry("900x600")

    canvas = tk.Canvas(root)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas_frame.bind("<Configure>", on_configure)
    canvas.configure(yscrollcommand=scrollbar.set)

    refresh_table()
    root.mainloop()



def login_form():
    def submit_login():
        email = email_entry.get()
        password = password_entry.get()
        if not email or not password:
            messagebox.showwarning("Eksik Bilgi", "Lütfen e-posta ve şifre giriniz.")
        else:
            login_window.destroy()
            fetch_posts(email, password)

    login_window = tk.Tk()
    login_window.title("LinkedIn Giriş")
    login_window.geometry("300x200")

    tk.Label(login_window, text="E-posta:").pack(pady=5)
    email_entry = tk.Entry(login_window, width=30)
    email_entry.pack(pady=5)

    tk.Label(login_window, text="Şifre:").pack(pady=5)
    password_entry = tk.Entry(login_window, width=30, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Giriş Yap", command=submit_login).pack(pady=10)

    login_window.mainloop()

# Uygulamayı başlat
login_form()
