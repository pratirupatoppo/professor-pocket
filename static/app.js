const form = document.querySelector("#chat-form");
const input = document.querySelector("#question");
const conversation = document.querySelector("#conversation");
const submitButton = form.querySelector("button[type='submit']");

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
  } catch (error) {
    conversation.lastElementChild.remove();
    addMessage("The chatbot service could not be reached. Check the Flask server.", "assistant");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "ASK ⚡";
  }
});
