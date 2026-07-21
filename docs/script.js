document.querySelectorAll('[data-compare]').forEach((compare) => {
  const range = compare.querySelector('input[type="range"]');
  const update = () => compare.style.setProperty('--position', `${range.value}%`);
  range.addEventListener('input', update);
  update();
});

const lightbox = document.querySelector('#lightbox');
const lightboxImage = lightbox.querySelector('img');

document.querySelectorAll('[data-lightbox]').forEach((button) => {
  button.addEventListener('click', () => {
    lightboxImage.src = button.dataset.lightbox;
    lightboxImage.alt = button.querySelector('img').alt;
    lightbox.showModal();
  });
});

lightbox.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
lightbox.addEventListener('click', (event) => {
  if (event.target === lightbox) lightbox.close();
});

const copyButton = document.querySelector('#copyPrompt');
copyButton.addEventListener('click', async () => {
  const prompt = document.querySelector('#promptText').textContent.trim();
  try {
    await navigator.clipboard.writeText(prompt);
    copyButton.textContent = '已复制';
  } catch {
    copyButton.textContent = '请手动复制';
  }
  window.setTimeout(() => { copyButton.textContent = '复制通用提示词'; }, 1800);
});
