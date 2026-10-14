# Selenium LinkedIn Post Fetcher

Bir LinkedIn şirket sayfasındaki gönderileri Selenium ile toplayıp küçük bir
masaüstü penceresinde (Tkinter) listeleyen deneme uygulaması.

## Ne yapıyor

1. Açılan pencerede LinkedIn e-posta adresini ve şifreni istiyor.
2. Chrome'u Selenium ile açıp LinkedIn'e giriş yapıyor.
3. Şirket sayfasının gönderi akışını sonuna kadar kaydırıyor; her gönderinin
   paylaşanını, açıklamasını, metnini ve varsa görselini topluyor.
4. Gönderileri bir tabloda gösteriyor. Her satırda iki düğme var:
   - **Listeden Çıkart:** gönderiyi listeden kaldırır.
   - **Sisteme Gönder:** şimdilik yalnızca bir bilgi kutusu gösterip gönderiyi
     listeden kaldırır; gerçek bir gönderim yapılmıyor.

## Kurulum

Python 3 ve Google Chrome gerekli. ChromeDriver'ı `webdriver-manager`
kendisi indiriyor.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Tkinter Python ile birlikte geliyor; bazı Linux dağıtımlarında ayrıca kurmak
gerekebilir (ör. `sudo apt install python3-tk`).

## Ayar

Hangi şirketin gönderilerinin çekileceği `app.py` içinde sabit yazılı:

```python
driver.get("https://www.linkedin.com/company/sicpa-assan/posts/?feedView=all")
```

Başka bir sayfa için bu adresi değiştirmen yeterli.

## Notlar

- E-posta ve şifre yalnızca açılan pencerede kullanılıyor; diske yazılmıyor.
- LinkedIn sayfa yapısını (CSS sınıflarını) değiştirdiğinde XPath seçicileri
  çalışmayabilir.
- LinkedIn'in kullanım koşulları otomatik veri toplamayı kısıtlıyor;
  uygulamayı kişisel denemeler için ve kendi sorumluluğunda kullan.
