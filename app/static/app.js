const chatWindow = document.getElementById("chat-window");
const questionInput = document.getElementById("question");
const sendBtn = document.getElementById("send-btn");
const customerSelect = document.getElementById("customer");

function appendMessage(text, sender) {
  const msg = document.createElement("div");
  msg.className = `chat-message ${sender}`;
  msg.textContent = text;
  chatWindow.appendChild(msg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendQuestion() {
  const question = questionInput.value.trim();
  if (!question) return;

  const customerId = customerSelect.value;
  appendMessage(question, "user");
  questionInput.value = "";

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ customer_id: customerId, question }),
    });

    if (!response.ok) {
      appendMessage("Sorry, Spending Insights is temporarily unavailable.", "bot");
      return;
    }

    const data = await response.json();
    appendMessage(data.answer, "bot");
  } catch (err) {
    appendMessage("Something went wrong reaching Spending Insights.", "bot");
    console.error(err);
  }
}

sendBtn.addEventListener("click", sendQuestion);
questionInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendQuestion();
});
