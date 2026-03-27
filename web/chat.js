
import { ChatComposer } from "/web/chat-composer.js";

const chat = new ChatComposer("msg-1");

// Optional configuration
chat.setPlaceholder("Ask me anything...");
chat.setHint("Press Enter to send");

// Attach custom backend logic
chat.setOnSubmit(async (text, instance) => {
  // Example: simulate API call
  await new Promise((resolve) => setTimeout(resolve, 500));

  // Append assistant response
  instance.appendMessage(`Echo: ${text}`, "assistant");
});

chat.init();