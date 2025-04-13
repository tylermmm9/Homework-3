document.addEventListener("DOMContentLoaded", () => {
  const socket = io(window.location.origin + '/chat', {
    transports: ['polling'],
    secure: true
  });
  const chatBox = document.getElementById("chat");
  
    socket.on('connect', () => {
      socket.emit('joined', {});
    });
  
    socket.on('status', (data) => {
      appendMessage(data.msg, data.role);
    });
  
    socket.on('chat', (data) => {
      appendMessage(data.msg, data.role);
    });
  
    const msgForm = document.getElementById("msgbrd");
    msgForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const input = document.getElementById("msg");
      const msg = input.value.trim();
      if (msg !== "") {
        socket.emit("send", msg);
        input.value = "";
      }
    });
  
    document.querySelector(".leave-btn").addEventListener("click", () => {
      socket.emit("leave");
      window.location.href = "/home";
    });
  
    function appendMessage(text, className) {
      const p = document.createElement("p");
      p.classList.add(className);
      p.textContent = text;
      chatBox.appendChild(p);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  });
  