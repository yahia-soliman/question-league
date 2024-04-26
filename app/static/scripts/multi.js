import { io } from "https://cdn.socket.io/4.7.5/socket.io.esm.min.js";

window.addEventListener("load", function () {
  const startBtn = document.querySelector("button")

  startBtn.onclick = () => {
    console.log("connecting...")
    const socket = io()
    socket.on("connect", () => {
      console.log("connected")
      window.socket = socket
    })
  }
})
