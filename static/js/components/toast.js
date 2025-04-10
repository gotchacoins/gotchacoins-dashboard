document.addEventListener("DOMContentLoaded", () => {
  const toasts = document.querySelectorAll(".toast");

  toasts.forEach((toast) => {
    const removeDelay = 1000;
    const fadeDuration = 500;

    setTimeout(() => {
      toast.style.transition = `opacity ${fadeDuration}ms ease`;
      toast.style.opacity = "0";

      setTimeout(() => {
        toast.remove();
      }, fadeDuration);
    }, removeDelay);
  });
});
