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
      this.handlers[event]?.forEach((func) => func(payload));
    });
  }

  on(event, cb) {
    if (["open", "close", "error", "message"].includes(event)) {
      return this.addEventListener(event, cb);
    }
    if (!this.handlers[event]) this.handlers[event] = [];
    this.handlers[event].push(cb);
  }

  emit(event, payload) {
    const message = { event, payload };
    this.send(JSON.stringify(message));
  }

  unbind(event) {
    delete this.handlers[event];
    console.log(this.handlers);
  }
}

/*
    <div class="min-h-8 flex group ready items-center justify-between pr-2">
      <h3 class="font-bold">Ahmed</h3>
      <span
        class="hidden border bg-white border-teal-300 rounded-full px-1 text-slate-500 group-[.ready]:inline font-mono text-xs h-min">ready</span>
    </div>
*/
const createUserCard = (user) => {
  let child;
  const card = document.createElement("div");

  card.dataset.id = user.user_id;
  card.className = "min-h-8 flex group items-center justify-between pr-2";
  if (user.ready) card.classList.append("ready");

  child = document.createElement("h3");
  child.innerText = user.user_id;
  child.className = "font-bold";
  card.append(child);

  child = document.createElement("span");
  child.innerText = "ready";
  child.className =
    "hidden border bg-white border-teal-300 rounded-full px-1 text-slate-500 group-[.ready]:inline font-mono text-xs h-min";
  card.append(child);
  return card;
};

const url = location.host + location.pathname;
const ws = new BetterSocket("ws://" + url);
ws.on("open", () => console.log("connected. via websocket."));
console.log("connecting...");
ws.on("message", (e) => console.log(e.data));
window.mysocket = ws;

window.addEventListener("load", () => {
  const users = document.getElementById("players");
  const categories = document.getElementById("categories");

  ws.on("welcome", (payload) => {
    payload.users.map((u) => users.append(createUserCard(u)));
    const c_ids = Object.keys(payload.categories);
    c_ids.sort((a, b) => payload.categories[b] - payload.categories[a]);
    c_ids.map((id) => {
      const elem = categories.children.find((e) => e.datased.categoryId == id);
      elem.lastChild.innerText = "- " + "&bullet;".repeat(c.votes);
      categories.prepend(elem);
    });
    ws.unbind("welcome");
  });

  ws.on("user_in", (payload) => {
    users.append(createUserCard(payload));
  });

  ws.on("user_out", (payload) => {
    users.find((el) => el.dataset.user_id == payload)?.remove();
  });

  ws.on("user_ready", (id) => {
    const user = users.querySelector(`[data-id="${id}"]`);
    user.classList.toggle("ready");
  });

  document.getElementById("start-game").onclick = () => ws.emit("ready");
  document.getElementById("invite-link").innerText = url;
  document.getElementById("copy-link").onclick = () => {
    navigator.clipboard.writeText(url);
  };
});
