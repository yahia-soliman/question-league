import { io } from "https://cdn.socket.io/4.7.5/socket.io.esm.min.js";
const socket = io();
console.log("connecting...")
socket.on("connect", (...args) => {
  console.log("connected: ", args);
  window.socketio = socket;
});

socket.on("ready", (...data) => {
  console.log("Ready: ", data)
});

window.addEventListener("load", function () {
  const startBtn = document.querySelector("#start");
  startBtn.onclick = () => {
    socket.emit('start');
  }
})
