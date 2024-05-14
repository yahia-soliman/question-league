const getQuestion = async (c_id = 0) => {
  const res = await fetch("/api/v1/questions?c=" + c_id);
  return await res.json();
};

const answerQuestion = async (q_id, answer) => {
  const res = await fetch(`/api/v1/questions/${q_id}`, {
    method: "POST",
    body: answer,
  });
  return await res.json();
};

window.addEventListener("load", () => {
  let skipTimeoutId = 0;
  const categories = document.getElementById("categories");
  const warn = document.getElementById("no-category-warn");
  const question = {
    id: null,
    c_id: categories.dataset.categoryId || 0,
    question: document.getElementById("question"),
    answers: document.getElementById("question-answers"),
    points: document.getElementById("question-points"),
  };

  const renderQuestion = async () => {
    clearTimeout(skipTimeoutId);
    payload = await getQuestion(question.c_id);
    question.id = payload.id;
    question.question.innerHTML = payload.question;
    question.points.innerText = payload.points;
    question.answers.innerHTML = "";
    payload.answers.forEach((answer) => {
      const elem = document.createElement("button");
      elem.innerHTML = answer;
      elem.className =
        "btn-sec bg-sky-100 rounded-xl mt-2 min-w-[48%] md:w-[49%] w-full";
      question.answers.append(elem);
      elem.onclick = async function () {
        const { points } = await answerQuestion(question.id, answer);
        if (points) skipTimeoutId = setTimeout(renderQuestion, 800);
        this.classList.add(points ? "bg-green-300" : "bg-red-300");
        this.classList.remove("bg-sky-100");
        this.onclick = null;
      };
    });
  };

  if (warn) {
    categories.addEventListener(
      "change",
      () => {
        warn.remove();
        question.question.parentElement.classList.remove("hidden");
        renderQuestion();
      },
      { once: true },
    );
  } else renderQuestion();

  categories.addEventListener("change", (e) => {
    question.c_id = e.target.value;
    renderQuestion();
  });
  document.getElementById("skip-question").onclick = renderQuestion;
});
