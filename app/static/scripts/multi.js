let room = null;

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

const createUserCard = (user) => {
  let child;
  const card = document.createElement("div");

  card.dataset.id = user.user_id;
  card.className = "min-h-8 flex group items-center justify-between pr-2";

  child = document.createElement("h3");
  child.innerText = user.name || user.user_id;
  child.className = "font-bold";
  card.append(child);

  if (!room.started) {
    if (user.ready) card.classList.add("ready");
    child = document.createElement("span");
    child.innerText = "ready";
    child.className =
      "hidden border bg-white border-teal-300 rounded-full px-1 text-slate-500 group-[.ready]:inline font-mono text-xs h-min";
    card.append(child);
  }
  child = document.createElement("span");
  child.innerText = user.score || "";
  child.className = "score text-yellow-700 font-mono font-semibold h-min";
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
  const question = {
    question: document.getElementById("question"),
    answers: document.getElementById("question-answers"),
    points: document.getElementById("question-points"),
    timer: document.getElementById("question-timer"),
    answer: null,
  };

  const sortCategories = (votes) => {
    categoryElems.forEach((elem) => {
      const id = elem.dataset.categoryId;
      elem.lastElementChild.innerHTML = "- " + "&bullet;".repeat(votes[id]);
      elem.dataset.votes = votes[id] || 0;
    });
    categoryElems.sort((a, b) => {
      const diff = b.dataset.votes - a.dataset.votes;
      if (diff) return diff;
      return a.dataset.name?.localeCompare(b.dataset.name);
    });
    categories.append(...categoryElems);
  };

  // WebSocket Event Listeners
  ws.on("welcome", (payload) => {
    room = payload;
    room.users.map((u) => users.append(createUserCard(u)));
    if (room.started) {
      questionHandler(room.question);
      setInterval(() => question.timer.innerText--, 1000);
    }
    sortCategories(payload.categories);
    if (room.user_id.endsWith("(guest)")) {
      document
        .getElementById("guest-name")
        ?.addEventListener("submit", function (e) {
          e.preventDefault();
          const name = this.firstElementChild.value;
          const fullname = name + " (guest)";
          if (
            room.users.find((u) => u.name == fullname || u.user_id == fullname)
          ) {
            alert(`this name is used`);
            return;
          }
          ws.emit("guest_name", { name });
          this.parentElement.remove();
        });
    }
    ws.unbind("welcome");
  });

  ws.on("user_in", (payload) => {
    users.append(createUserCard(payload));
    room.users.push(payload);
  });

  ws.on("user_out", (id) => {
    users.querySelector(`[data-id="${id}"]`).remove();
  });

  ws.on("guest_name", (payload) => {
    const user = users.querySelector(`[data-id="${payload.user_id}"]`);
    if (!user) return;
    user.firstChild.innerText = payload.name;
    room.users.find((u) => u.user_id == payload.user_id).name = payload.name;
  });

  ws.on("user_ready", (payload) => {
    const user = users.querySelector(`[data-id="${payload.user_id}"]`);
    user.classList.toggle("ready", payload.ready);
  });

  ws.on("votes", sortCategories);

  ws.on("game_start", () => {
    ws.unbind("ready");
    setInterval(() => question.timer.innerText--, 1000);
    question.question.parentElement.classList.remove("hidden");
    document.getElementById("start-game")?.parentElement.remove();
    [...users.children].forEach((u) => u.classList.remove("ready"));
  });
  const questionHandler = (payload) => {
    question.answer = null;
    question.question.innerHTML = payload.question;
    question.points.innerText = payload.points;
    question.timer.innerText = 30;
    question.answers.innerHTML = "";
    payload.answers.forEach((answer) => {
      const elem = document.createElement("button");
      elem.innerHTML = answer;
      elem.className = "btn-sec bg-sky-100 rounded-xl mt-2 min-w-[48%]";
      question.answers.append(elem);
    });
    question.answers.onclick = function ({ target }) {
      if (target === this) return;
      ws.emit("answer", { answer: target.innerHTML });
      question.answers.onclick = null;
      question.answer = target;
    };
    [...users.children].forEach((elem) =>
      elem.classList.remove("bg-green-200", "bg-red-100"),
    );
  };
  ws.on("question", questionHandler);
  ws.on("user_answer", (payload) => {
    const user = users.querySelector(`[data-id="${payload.user_id}"]`);
    const user_score = user.querySelector(".score");
    user_score.innerText = Number(user_score.innerText) + payload.score;
    user.classList.add(payload.score ? "bg-green-200" : "bg-red-100");
    if (payload.user_id === room.user_id) {
      question.answer?.classList.add(
        payload.score ? "bg-green-300" : "bg-red-300",
      );
      question.answer?.classList.remove("bg-sky-100");
    }
  });

  // DOM Event Listeners
  document.getElementById("start-game").onclick = () => ws.emit("ready");
  document.getElementById("invite-link").innerText = url;
  document.getElementById("copy-link").onclick = () => {
    navigator.clipboard.writeText(url);
  };
  categories.addEventListener("change", (e) => {
    ws.emit("category_vote", { category_id: e.target.value });
  });
});
