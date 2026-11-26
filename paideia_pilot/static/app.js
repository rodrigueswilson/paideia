const byId = (id) => document.getElementById(id);
const status = byId("status");
let current = null;
let hintUsed = false;
let pendingAttempt = null;
let sessionEnd = 0;
let timerHandle = null;

function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `Request failed (${response.status})`);
  return data;
}

function post(path, body = {}) {
  return request(path, { method: "POST", body: JSON.stringify(body) });
}

function say(message) { status.textContent = message; }

async function refresh() {
  const data = await request("/api/state");
  byId("counts").textContent = `${data.summary.documents} document · ${data.summary.approved}/${data.summary.objects} approved objects · ${data.summary.attempts} attempts`;
  const list = byId("objects");
  list.replaceChildren();
  for (const object of data.objects) {
    const item = el("article", undefined, "object");
    item.append(el("h3", `Passage ${object.position + 1}`));
    item.append(el("blockquote", object.quote));
    item.append(el("p", object.question));
    item.append(el("p", `Fixture answer: ${object.expected_answer}`, "meta"));
    item.append(el("p", `Origin: ${object.origin} · PDF hash: ${object.document_id.slice(0, 12)} · extraction: ${object.extractor}`, "meta"));
    if (object.status === "approved") {
      item.append(el("span", "Approved", "badge"));
    } else {
      const button = el("button", "Approve for study");
      button.addEventListener("click", async () => {
        try {
          await post(`/api/objects/${encodeURIComponent(object.id)}/approve`);
          say(`Passage ${object.position + 1} approved.`);
          await refresh();
        } catch (error) { say(error.message); }
      });
      item.append(button);
    }
    list.append(item);
  }
}

byId("import-btn").addEventListener("click", async () => {
  try {
    const result = await post("/api/import-sample");
    say(`Synthetic PDF imported. ${result.objects.length} draft objects are ready for inspection.`);
    await refresh();
  } catch (error) { say(error.message); }
});

function tick() {
  const remaining = Math.max(0, Math.ceil((sessionEnd - Date.now()) / 1000));
  byId("timer").textContent = `${Math.floor(remaining / 60)}:${String(remaining % 60).padStart(2, "0")}`;
  if (remaining === 0) {
    clearInterval(timerHandle);
    byId("timer").textContent = "Session time reached";
  }
}

async function showNext() {
  const data = await request("/api/next");
  const card = byId("study-card");
  card.replaceChildren();
  card.hidden = false;
  current = data.next;
  hintUsed = false;
  pendingAttempt = null;
  if (!current) {
    card.append(el("p", "No pending questions. Approve more passages or start another session later."));
    return;
  }
  card.append(el("p", current.rationale, "meta"));
  card.append(el("p", current.question, "question"));
  const hint = el("button", "Show source passage as hint");
  hint.addEventListener("click", () => {
    hintUsed = true;
    hint.replaceWith(el("blockquote", current.quote));
  });
  card.append(hint);
  const reveal = el("button", "Reveal fixture answer", "primary");
  reveal.addEventListener("click", () => {
    reveal.replaceWith(el("div", current.expected_answer, "answer"));
    addRatings(card);
  });
  card.append(el("span", " "));
  card.append(reveal);
  const skip = el("button", "Skip");
  skip.addEventListener("click", () => rate("skip"));
  card.append(el("span", " "));
  card.append(skip);
}

function addRatings(card) {
  const row = el("div", undefined, "rating-row");
  for (const [value, label] of [
    ["matched", "My answer matched"], ["partial", "Partly matched"], ["not_yet", "Not yet"],
  ]) {
    const button = el("button", label);
    button.addEventListener("click", () => rate(value));
    row.append(button);
  }
  card.append(row);
}

async function rate(rating) {
  if (!current) return;
  if (!pendingAttempt) {
    pendingAttempt = {
      attempt_id: crypto.randomUUID(), event_id: crypto.randomUUID(),
      presentation_id: current.presentation_id, object_id: current.id,
      object_version: current.version, rating, used_hint: hintUsed,
    };
  }
  try {
    await post("/api/attempts", pendingAttempt);
    say("Attempt saved. Your typed answer was not collected.");
    await refresh();
    await showNext();
  } catch (error) {
    say(`${error.message}. Retry uses the same attempt ID.`);
    const retry = el("button", "Retry saving");
    retry.addEventListener("click", () => rate(rating));
    byId("study-card").append(retry);
  }
}

byId("start-btn").addEventListener("click", async () => {
  sessionEnd = Date.now() + Number(byId("minutes").value) * 60000;
  clearInterval(timerHandle);
  timerHandle = setInterval(tick, 1000);
  tick();
  try { await showNext(); } catch (error) { say(error.message); }
});

refresh().catch((error) => say(error.message));
