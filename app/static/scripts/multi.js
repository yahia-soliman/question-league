class BetterSocket extends WebSocket {

  constructor(...props) {
    super(...props);
    this.handlers = {};
    this.addEventListener("message", (e) => {
      let event, payload;
      try {
        const data = JSON.parse(e.data);
        event = data.event;
        payload = data.payload;
      } catch {
        event = "message";
        payload = e;
      }
      this.handlers[event]?.forEach((func) => func(payload))
    });
  }

  on(event, cb) {
    if (["open", "close", "error", "message"].includes(event)) {
      return this.addEventListener(event, cb);
    }
    if (!this.handlers[event])
      this.handlers[event] = [];
    this.handlers[event].push(cb);
  }

  emit(event, payload) {
    const message = { event, payload }
    this.send(JSON.stringify(message))
  }
}

const createUserCard = (user) => {
  let child;
  const card = document.createElement("div");

  card.dataset.id = user.user_id;
  card.classList.add("group");

  child = document.createElement("h3");
  child.innerText = user.user_id;
  card.append(child);

  child = document.createElement("span");
  child.innerText = "✓";
  child.classList.add("hidden", "group-[.ready]:inline");
  card.append(child);

  return card;
}

const ws = new BetterSocket("ws://" + location.host + location.pathname)
ws.on("open", () => console.log("connected. via websocket."))
console.log("connecting...")
ws.on("message", (e) => console.log(e.data))
window.mysocket = ws;

window.addEventListener("load", () => {
  const start = document.querySelector("#start-game");
  const users = document.querySelector("#players");

  start.onclick = () => ws.emit("ready");

  ws.on("user_in", (payload) => {
    users.append(createUserCard(payload));
  })
  ws.on("user_ready", (id) => {
    const user = users.querySelector(`[data-id="${id}"]`);
    user.classList.toggle("ready");
  })
})
