const form = document.querySelector("#chat-form");
const input = document.querySelector("#question");
const conversation = document.querySelector("#conversation");
const submitButton = form.querySelector("button[type='submit']");
const soundToggle = document.querySelector("#sound-toggle");
let audioContext;
let soundEnabled = true;
const funFacts = [
  ["Make your people", "The best friendships can start with a shared class, a residence corridor, or a simple “want to grab food?”"],
  ["The syllabus side quest", "A college day can begin with one planned class and somehow unlock three unexpected conversations."],
  ["Campus compass", "Every student eventually develops a personal map of shortcuts, snack spots, and “meet me here” landmarks."],
  ["The five-minute friend", "A quick chat before class can become a study partner, a project teammate, or a lifelong friend."],
  ["Club curiosity", "Trying one new club or event is one of the easiest ways to turn a big campus into a smaller community."],
  ["Snack science", "Many brilliant campus ideas begin with two ingredients: a deadline and something crunchy."],
  ["Library magic", "The quietest corner of campus often has the loudest collection of ideas."],
  ["Group project lore", "Every group project has a planner, a researcher, a designer, and one person who says “I’ll make the slides.”"],
  ["Rainy-day bonding", "Unexpected weather has a funny way of turning strangers sharing shelter into temporary teammates."],
  ["The residence network", "A residence hallway can become a mini community powered by borrowed chargers and shared recommendations."],
  ["Event energy", "The best campus memories are often the ones you almost skipped."],
  ["Study break rule", "A good study break should refresh your brain, not become a four-hour documentary marathon. Usually."],
  ["Campus soundtrack", "Every student has a route, a playlist, and a preferred speed for walking to class."],
  ["Kindness shortcut", "Sharing notes, directions, or a seat can make a new campus feel friendly in seconds."],
  ["Deadline physics", "The closer the deadline gets, the faster snacks disappear and keyboard sounds multiply."],
  ["Curiosity wins", "Ask one extra question today. It might lead to a new skill, a new place, or a new friend."],
  ["Tiny traditions", "The small routines you repeat with friends often become the stories you remember most."],
  ["Main-character moment", "College is part classroom, part community, and part figuring things out as you go."]
];
let funFactIndex = 0;

function enableSound() {
  if (!audioContext) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return false;
    audioContext = new AudioContext();
  }
  if (audioContext.state === "suspended") audioContext.resume();
  return true;
}

function playSound(frequencies, duration = 0.1) {
  if (!soundEnabled || !enableSound()) return;
  const oscillator = audioContext.createOscillator();
  const gain = audioContext.createGain();
  oscillator.type = "square";
  oscillator.frequency.setValueAtTime(frequencies[0], audioContext.currentTime);
  frequencies.slice(1).forEach((frequency, index) => {
    oscillator.frequency.setValueAtTime(
      frequency,
      audioContext.currentTime + (duration / frequencies.length) * (index + 1),
    );
  });
  gain.gain.setValueAtTime(0.2, audioContext.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);
  oscillator.connect(gain);
  gain.connect(audioContext.destination);
  oscillator.start();
  oscillator.stop(audioContext.currentTime + duration);
}

document.querySelectorAll("button").forEach((button) => {
  if (button !== soundToggle) {
    button.addEventListener("click", () => playSound([520, 700], 0.07));
  }
});

soundToggle.addEventListener("click", () => {
  soundEnabled = !soundEnabled;
  if (soundEnabled) enableSound();
  soundToggle.textContent = soundEnabled ? "🔊 SOUND ON" : "🔇 SOUND OFF";
  soundToggle.setAttribute("aria-pressed", String(soundEnabled));
  if (soundEnabled) playSound([587, 784], 0.12);
});

const animatedSections = document.querySelectorAll(".hero-copy, .hero-art, .chat-card, .specs-copy, .spec-grid, .fun-card");
animatedSections.forEach((element) => element.classList.add("reveal"));
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("revealed");
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
animatedSections.forEach((element) => revealObserver.observe(element));

function rotateFunFact() {
  const card = document.querySelector("#fun-fact-card");
  const title = document.querySelector("#fun-fact-title");
  const text = document.querySelector("#fun-fact-text");
  const count = document.querySelector("#fun-fact-count");
  if (!card || !title || !text || !count) return;
  funFactIndex = (funFactIndex + 1) % funFacts.length;
  card.classList.remove("is-changing");
  void card.offsetWidth;
  title.textContent = funFacts[funFactIndex][0];
  text.textContent = funFacts[funFactIndex][1];
  count.textContent = `${String(funFactIndex + 1).padStart(2, "0")} / ${funFacts.length}`;
  card.classList.add("is-changing");
}

window.setInterval(rotateFunFact, 8000);

function addMessage(text, kind) {
  const message = document.createElement("div");
  message.className = `message ${kind}`;
  message.textContent = text;
  conversation.appendChild(message);
  message.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

document.querySelectorAll("[data-question]").forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.dataset.question;
    input.focus();
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (!question) return;
  addMessage(question, "user");
  playSound([440, 660], 0.12);
  input.value = "";
  submitButton.disabled = true;
  submitButton.textContent = "THINKING...";
  addMessage("Searching the campus knowledge base...", "assistant");
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const payload = await response.json();
    conversation.lastElementChild.remove();
    addMessage(payload.answer || payload.error || "The assistant could not answer.", "assistant");
    playSound([660, 880], 0.16);
  } catch (error) {
    conversation.lastElementChild.remove();
    addMessage("The chatbot service could not be reached. Check the Flask server.", "assistant");
    playSound([330, 220], 0.18);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "ASK ⚡";
  }
});
