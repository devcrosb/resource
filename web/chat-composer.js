/**
 * ChatComposer
 * -------------
 * A self-contained chat input + message display component.
 *
 * Features:
 * - Auto-resizing textarea input
 * - Enter to send, Shift+Enter for newline
 * - Built-in browser spellcheck support
 * - Disabled state during async submission
 * - Internal default behavior (can be overridden)
 * - Fully renders its own UI inside a container div
 *
 * Usage:
 *
 * HTML:
 *   <div id="input-id"></div>
 *
 * JavaScript:
 *   import { ChatComposer } from "./chat-composer.js";
 *
 *   const chat = new ChatComposer("input-id");
 *
 *   // Optional configuration
 *   chat.setPlaceholder("Ask something...");
 *   chat.setHint("Enter to send");
 *   chat.setOnSubmit(async (text, instance) => {
 *     instance.appendMessage("Processing...", "assistant");
 *   });
 *
 *   chat.init();
 *
 * Notes:
 * - This component does NOT include networking by default.
 * - Override `setOnSubmit()` to connect to your backend.
 * - Messages are appended using `appendMessage(text, role)`
 */


export class ChatComposer {
  /**
   * @param {string} inpID - The ID of the container element
   * where the component will be rendered.
   */
  constructor(inpID) {
    this.container = document.getElementById(inpID);

    if (!this.container) {
      throw new Error(`Container element not found: #${inpID}`);
    }

    // ---------- Internal Defaults ----------
    this.placeholder = "Message ChatGPT";
    this.hintText = "Enter to send • Shift+Enter for a new line";
    this.onSubmitHandler = this.defaultOnSubmit.bind(this);

    // ---------- Internal State ----------
    this.isSending = false;

    // DOM references (assigned during render)
    this.root = null;
    this.messages = null;
    this.composer = null;
    this.input = null;
    this.sendBtn = null;
    this.hintEl = null;

    // Bind handlers once to preserve context
    this.handleInput = this.handleInput.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  // =========================================================
  // Public Configuration API
  // =========================================================

  /**
   * Set a custom submit handler.
   * This function is called when the user sends a message.
   *
   * @param {Function} fn - async (text, instance) => {}
   */
  setOnSubmit(fn) {
    if (typeof fn === "function") {
      this.onSubmitHandler = fn;
    }
  }

  /**
   * Set placeholder text for the input field.
   */
  setPlaceholder(text) {
    this.placeholder = text;
    if (this.input) {
      this.input.placeholder = text;
    }
  }

  /**
   * Set the hint text displayed below the input.
   */
  setHint(text) {
    this.hintText = text;
    if (this.hintEl) {
      this.hintEl.textContent = text;
    }
  }

  /**
   * Initialize and render the component.
   * Must be called after instantiation.
   */
  init() {
    this.render();
    this.bindEvents();
    this.autoResize();
    this.setSendingState(false);
  }

  /**
   * Clean up DOM and event listeners.
   */
  destroy() {
    if (this.input) {
      this.input.removeEventListener("input", this.handleInput);
      this.input.removeEventListener("keydown", this.handleKeyDown);
    }

    if (this.composer) {
      this.composer.removeEventListener("submit", this.handleSubmit);
    }

    if (this.root && this.container.contains(this.root)) {
      this.container.removeChild(this.root);
    }
  }

  // =========================================================
  // Rendering
  // =========================================================

  /**
   * Build and inject the component DOM.
   * This replaces the contents of the container element.
   */
  render() {
    this.container.innerHTML = "";

    this.root = document.createElement("div");
    this.root.className = "chat-shell";

    // Messages container
    this.messages = document.createElement("div");
    this.messages.className = "messages";

    // Form (composer)
    this.composer = document.createElement("form");
    this.composer.className = "composer";
    this.composer.setAttribute("novalidate", "");

    const inputWrap = document.createElement("div");
    inputWrap.className = "input-wrap";

    // Text input
    this.input = document.createElement("textarea");
    this.input.className = "chat-input";
    this.input.rows = 1;
    this.input.placeholder = this.placeholder;

    // Enable browser spellcheck + typing improvements
    this.input.spellcheck = true;
    this.input.setAttribute("autocorrect", "on");
    this.input.setAttribute("autocomplete", "on");
    this.input.setAttribute("autocapitalize", "sentences");
    this.input.setAttribute("enterkeyhint", "send");

    // Send button
    this.sendBtn = document.createElement("button");
    this.sendBtn.className = "send-btn";
    this.sendBtn.type = "submit";
    this.sendBtn.textContent = "↑";

    // Hint text
    this.hintEl = document.createElement("div");
    this.hintEl.className = "hint";
    this.hintEl.textContent = this.hintText;

    // Assemble DOM
    inputWrap.appendChild(this.input);
    this.composer.appendChild(inputWrap);
    this.composer.appendChild(this.sendBtn);

    this.root.appendChild(this.messages);
    this.root.appendChild(this.composer);
    this.root.appendChild(this.hintEl);

    this.container.appendChild(this.root);
  }

  /**
   * Attach DOM event listeners.
   */
  bindEvents() {
    this.input.addEventListener("input", this.handleInput);
    this.input.addEventListener("keydown", this.handleKeyDown);
    this.composer.addEventListener("submit", this.handleSubmit);
  }

  // =========================================================
  // Event Handlers
  // =========================================================

  /**
   * Handle typing input:
   * - Resize textarea
   * - Toggle send button state
   */
  handleInput() {
    this.autoResize();
    this.sendBtn.disabled = this.isSending || !this.input.value.trim();
  }

  /**
   * Handle keyboard input:
   * - Enter submits
   * - Shift+Enter inserts newline
   */
  handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      this.submitMessage();
    }
  }

  /**
   * Handle form submission (button click or Enter).
   */
  handleSubmit(event) {
    event.preventDefault();
    this.submitMessage();
  }

  // =========================================================
  // Core Behavior
  // =========================================================

  /**
   * Automatically resize textarea to fit content.
   */
  autoResize() {
    this.input.style.height = "0px";
    this.input.style.height = Math.min(this.input.scrollHeight, 220) + "px";
  }

  /**
   * Enable/disable UI while sending a message.
   */
  setSendingState(isSending) {
    this.isSending = isSending;
    this.input.disabled = isSending;
    this.sendBtn.disabled = isSending || !this.input.value.trim();
  }

  /**
   * Append a message to the message list.
   *
   * @param {string} text
   * @param {"user"|"assistant"} role
   */
  appendMessage(text, role = "user") {
    const node = document.createElement("div");
    node.className = "message";
    node.dataset.role = role;
    node.textContent = text;

    this.messages.appendChild(node);
    this.messages.scrollTop = this.messages.scrollHeight;
  }

  /**
   * Handle sending a message.
   */
  async submitMessage() {
    const text = this.input.value.trim();

    if (!text || this.isSending) return;

    // Show user message immediately
    this.appendMessage(text, "user");

    // Reset input
    this.input.value = "";
    this.autoResize();
    this.setSendingState(true);

    try {
      await this.onSubmitHandler(text, this);
    } catch (error) {
      console.error("Submit error:", error);
      this.appendMessage("Something went wrong.", "assistant");
    } finally {
      this.setSendingState(false);
      this.input.focus();
    }
  }

  /**
   * Default fallback submit handler.
   * Used if no custom handler is provided.
   */
  async defaultOnSubmit(text, instance) {
    await new Promise((resolve) => setTimeout(resolve, 500));
    instance.appendMessage(`You said: ${text}`, "assistant");
  }
}
