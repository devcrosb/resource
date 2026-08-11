
document.querySelectorAll(".expandable-text").forEach(container => {
  const text = container.querySelector(".text-content");
  const button = container.querySelector(".toggle-button");

  // Initially clamp it.
  text.classList.add("collapsed");

  // Hide button when there's nothing to expand.
  if (text.scrollHeight <= text.clientHeight) {
    button.hidden = true;
    return;
  }

  button.addEventListener("click", () => {
    const collapsed = text.classList.toggle("collapsed");

    button.textContent = collapsed ? "Show more" : "Show less";
    button.setAttribute("aria-expanded", String(!collapsed));
  });
});

