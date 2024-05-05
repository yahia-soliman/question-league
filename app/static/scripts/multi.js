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
  if (user.ready) card.classList.add("ready");

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
  const categoryElems = [...categories.children];

  const sortCategories = (votes) => {
    categoryElems.forEach((elem) => {
      const id = elem.dataset.categoryId;
      elem.lastElementChild.innerHTML = "- " + "&bullet;".repeat(votes[id]);
      if (votes[id]) votes[id] = elem;
    });
  };

  // WebSocket Event Listeners
  ws.on("welcome", (payload) => {
    payload.users.map((u) => users.append(createUserCard(u)));
    sortCategories(payload.categories);
    ws.unbind("welcome");
  });

  ws.on("user_in", (payload) => {
    users.append(createUserCard(payload));
  });

  ws.on("user_out", (id) => {
    users.querySelector(`[data-id="${id}"]`).remove();
  });

  ws.on("user_ready", (payload) => {
    const user = users.querySelector(`[data-id="${payload.user_id}"]`);
    user.classList.toggle("ready", payload.ready);
  });

  ws.on("votes", sortCategories);

  // DOM Event Listeners
  document.getElementById("start-game").onclick = () => ws.emit("ready");
  document.getElementById("invite-link").innerText = url;
  document.getElementById("copy-link").onclick = () => {
    navigator.clipboard.writeText(url);
  };
  categories.addEventListener("change", (e) => {
    console.log(e.target);
    ws.emit("category_vote", { category_id: e.target.value });
  });
});
