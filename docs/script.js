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

const filterDemo = document.querySelector('#filterDemo');
const coverageRange = document.querySelector('#coverageRange');
const recursionRange = document.querySelector('#recursionRange');
const coverageOutput = document.querySelector('#coverageOutput');
const recursionOutput = document.querySelector('#recursionOutput');
const filterCode = document.querySelector('#filterCode');

function updateFilterDemo() {
  const coverage = coverageRange.value;
  const recursion = recursionRange.value;
  filterDemo.dataset.intensity = coverage;
  filterDemo.dataset.recursion = recursion;
  coverageOutput.value = coverage;
  recursionOutput.value = recursion;
  const structure = Math.min(4, Number(coverage));
  const motion = Number(coverage) >= 3 ? 2 : Number(coverage) >= 1 ? 1 : 0;
  filterCode.textContent = `C${coverage}-S${structure}-R${recursion}-P5-M${motion}`;
}

coverageRange.addEventListener('input', updateFilterDemo);
recursionRange.addEventListener('input', updateFilterDemo);
updateFilterDemo();
