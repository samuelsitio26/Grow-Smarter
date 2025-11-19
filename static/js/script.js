function initTypingAnimation() {
  let currentTextIndex = 0;
  const texts = [
    "Grow Smarter:",
    "Predict the Best Crops & Soil Fertility",
  ];

  function typeText() {
    const typingTextElement = document.getElementById(`typingText${currentTextIndex + 1}`);
    if (!typingTextElement) return;

    let text = texts[currentTextIndex];
    let currentLetterIndex = 0;
    typingTextElement.textContent = '';

    const typingInterval = setInterval(() => {
      typingTextElement.textContent += text[currentLetterIndex];
      currentLetterIndex++;

      if (currentLetterIndex === text.length) {
        clearInterval(typingInterval);
        currentTextIndex++;

        if (currentTextIndex < texts.length) {
          setTimeout(typeText, 1000);
        }
      }
    }, 100);
  }
  
  window.onload = typeText;

  if (document.readyState === 'complete') {
    typeText();
  } else {
    document.addEventListener('DOMContentLoaded', typeText);
  }
}

function animateCounter(element, target, duration) {
  let start = 0;
  const step = () => {
    const progress = Math.min(start / duration, 1);
    const value = Math.floor(progress * target);
    element.textContent = `${value}%`;

    if (progress < 1) {
      start += 16;
      requestAnimationFrame(step);
    } else {
      element.textContent = `${target}%`;
    }
  };
  requestAnimationFrame(step);
}

function initAOS() {
  AOS.init({
    duration: 1000,
    once: false,
  });

  const accuracySection = document.getElementById('accuracySection');
  if (accuracySection) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const counterEl = document.getElementById('accuracyCounter');
        if (entry.isIntersecting && counterEl) {
          animateCounter(counterEl, 87, 1000);
        }
      });
    }, { threshold: 0.5 });

    observer.observe(accuracySection);
  }
}

function initProgressChart() {
  const ctx = document.getElementById('progressBar')?.getContext('2d');
  if (!ctx) {
    console.warn("Progress bar canvas not found");
    return;
  }

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      datasets: [{
        data: [86, 14],
        backgroundColor: ['#38a169', '#ddd'],
        borderWidth: 0,
        hoverOffset: 32,
      }]
    },
    options: {
      circumference: Math.PI * 57,
      rotation: -Math.PI / 0.035,
      cutout: '70%',
      responsive: true,
      plugins: {
        tooltip: { enabled: false },
        legend: { display: false },
      },
    }
  });
}

function init() {
  initTypingAnimation();
  initAOS();
  initProgressChart();
}

if (document.readyState === 'complete') {
  init();
} else {
  document.addEventListener('DOMContentLoaded', init);
}