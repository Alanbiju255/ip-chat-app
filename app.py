from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

# ✅ Force threading mode to avoid Redis/aioredis issues
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# HTML + CSS inside Python
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>IP Chat</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background: #222;
      color: #fff;
    }
    .chat-box {
      width: 400px;
      background: #333;
      border-radius: 10px;
      padding: 15px;
    }
    #messages {
      height: 250px;
      overflow-y: auto;
      background: #111;
      padding: 10px;
      border-radius: 5px;
      margin-bottom: 10px;
    }
    #msg {
      width: 70%;
      padding: 8px;
      border: none;
      border-radius: 5px;
    }
    button {
      width: 25%;
      padding: 8px;
      border: none;
      border-radius: 5px;
      background: #0af;
      color: #fff;
      cursor: pointer;
    }
    button:hover {
      background: #08c;
    }
  </style>
  <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
</head>
<body>
  <div class="chat-box">
    <h3>IP Chat</h3>
    <div id="messages"></div>
    <input id="msg" type="text" placeholder="Type a message...">
    <button onclick="sendMessage()">Send</button>
  </div>

  <script>
    const socket = io();

    socket.on("message", function(msg) {
      let messages = document.getElementById("messages");
      let newMsg = document.createElement("p");
      newMsg.textContent = msg;
      messages.appendChild(newMsg);
      messages.scrollTop = messages.scrollHeight;
    });

    function sendMessage() {
      let msg = document.getElementById("msg").value;
      if (msg.trim() !== "") {
        socket.send(msg);
      }
      document.getElementById("msg").value = "";
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html_code)

@socketio.on("message")
def handle_message(msg):
    user_ip = request.remote_addr
    print(f"{user_ip}: {msg}")
    send(f"{user_ip}: {msg}", broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
