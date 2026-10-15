const form = document.querySelector("#chat-form");
const input = document.querySelector("#question");
const conversation = document.querySelector("#conversation");
const submitButton = form.querySelector("button[type='submit']");
const soundToggle = document.querySelector("#sound-toggle");
let audioContext;
let soundEnabled = true;

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
  oscillator.type = "sine";
  oscillator.frequency.setValueAtTime(frequencies[0], audioContext.currentTime);
  frequencies.slice(1).forEach((frequency, index) => {
    oscillator.frequency.setValueAtTime(
      frequency,
      audioContext.currentTime + (duration / frequencies.length) * (index + 1),
    );
  });
  gain.gain.setValueAtTime(0.08, audioContext.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);
  oscillator.connect(gain);
  gain.connect(audioContext.destination);
  oscillator.start();
  oscillator.stop(audioContext.currentTime + duration);
}

soundToggle.addEventListener("click", () => {
  soundEnabled = !soundEnabled;
  if (soundEnabled) enableSound();
  soundToggle.textContent = soundEnabled ? "🔊 SOUND ON" : "🔇 SOUND OFF";
  soundToggle.setAttribute("aria-pressed", String(soundEnabled));
  if (soundEnabled) playSound([587, 784], 0.12);
});

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
