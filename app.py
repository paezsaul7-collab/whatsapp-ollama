from ollama_service import consultar_ollama
from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route('/saludar', methods=["GET"])
def saludar():
    return "Servidor funcionando Hi"

@app.route('/whatsapp', methods=["GET"])
def VerifyToken():
    try:
        access_token = "asdasd"
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == access_token:
            return challenge
        else:
            return "error", 400
    except:
        return "error", 400

def whatsappService(body):
    try:
        token = "EAASkRxvpiZBYBRQXTxZAE8DjB9VphLaJ6piOddLhCveDVh8ILLbvrOmOUdjUQZBYgNbOd1y54aQXfxdUQAgdMKxTnlOEvaN24ScNja04n53e94NZBJlGExAdRbmMwl39nsrVlG3EE1ZC9yJu14Coeumif6s60HTLlcnR0O2pdobBanAlWKZCV1Q9wZBladKhQZDZD"  # <-- reemplaza esto
        api_url = "https://graph.facebook.com/v22.0/1079140861955843/messages"  # <-- reemplaza esto
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(api_url, data=json.dumps(body), headers=headers)
        if response.status_code == 200:
            print("Mensaje enviado correctamente")
            return True
        else:
            print("Error al enviar el mensaje:", response.text)
            return False
    except Exception as e:
        print("Ocurrió un error con la API:", str(e))
        return False

def enviarmensaje(text, numero):
    respuesta = consultar_ollama(text)
    body = {
        "messaging_product": "whatsapp",    
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {
            "body": respuesta
        }
    }
    return body

@app.route('/whatsapp', methods=["POST"])
def RecibirMensaje():
    try:
        body = request.get_json()
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value["messages"][0]
        text = messages["text"]
        question_user = text["body"]
        number = messages["from"]
        print("Mensaje recibido:", question_user)
        body_answer = enviarmensaje(question_user, number)
        send_message = whatsappService(body_answer)
        if send_message:
            print("Mensaje enviado correctamente")
        else:
            print("Error al enviar el mensaje")
        return "EVENT_RECEIVED"
    except Exception as e:
        print("Ocurrió un error al procesar el mensaje:", str(e))
        return "EVENT_RECEIVED"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8502, debug=True)