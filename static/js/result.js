// DOM Elements
const form = document.getElementById("cropForm");
const predictedLabelElement = document.getElementById("predictedLabel");
const cropDescriptionElement = document.getElementById("cropDescription");
const fertilityScoreElement = document.getElementById("fertilityScore");
const fertilityCategoryElement = document.getElementById("fertilityCategory");
const resultSection = document.getElementById("result");
const cropImage = document.getElementById("predictedCropImage");
const scoreImage = document.getElementById("predictedScoreImage");
const infoPopupButton = document.getElementById("openInfoPopup");
const infoPopup = document.getElementById("infoPopup");
const closePopup = document.getElementById("closePopup");
const backButton = document.getElementById("backButton");
const infoButtonContainer = document.getElementById("infoButton");

const FERTILITY_CATEGORIES = [
  {
    min: 0,
    max: 25.9,
    category: "Very Low Fertility, indicates extremely low nutrient levels (N, P, K), severely limiting crop growth and yield potential.",
    image: "/static/assets/images/very-low-fertility.png"
  },
  {
    min: 26.0,
    max: 60.0,
    category: "Low Fertility, indicates insufficient nutrient levels (N, P, K) to support robust crop growth, limiting yield potential.",
    image: "/static/assets/images/low-fertility.png"
  },
  {
    min: 60.1,
    max: 90.0,
    category: "Moderate Fertility, suggests adequate nutrient availability, supporting decent crop development but not optimal productivity.",
    image: "/static/assets/images/moderate-fertility.png"
  },
  {
    min: 90.1,
    max: 120.0,
    category: "High Fertility, reflects high nutrient levels, ideal for maximizing crop yield and supporting vigorous plant growth.",
    image: "/static/assets/images/high-fertility.png"
  },
  {
    min: 120.1,
    max: Infinity,
    category: "Very High Fertility, indicates extremely high nutrient levels, which can lead to excessive growth and potential nutrient imbalances.",
    image: "/static/assets/images/very-high-fertility.png"
  }
];

document.addEventListener("DOMContentLoaded", () => {
  infoPopupButton.addEventListener("click", showInfoPopup);
  closePopup.addEventListener("click", hideInfoPopup);
  infoPopup.addEventListener("click", handlePopupClick);
  form.addEventListener("submit", handleFormSubmit);
  window.addEventListener("scroll", handleScroll);
});

// Functions
function showInfoPopup() {
  infoPopup.classList.remove("hidden");
}

function hideInfoPopup() {
  infoPopup.classList.add("hidden");
}

function handlePopupClick(e) {
  if (e.target === infoPopup) {
    hideInfoPopup();
  }
}

async function handleFormSubmit(e) {
  e.preventDefault();
  
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  
  for (let key in data) {
    data[key] = parseFloat(data[key]);
    if (isNaN(data[key])) {
      alert(`Please enter a valid number for ${key}`);
      return;
    }
  }

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    if (result.error) {
      throw new Error(result.error);
    }

    updateUIWithResults(result);
  } catch (error) {
    console.error("Error:", error);
    alert(`Failed to get prediction: ${error.message}`);
  }
}

function updateUIWithResults(result) {
  // Update cluster information
  predictedLabelElement.textContent = result.cluster_name;
  cropDescriptionElement.textContent = result.cluster_description || "Cluster information not available.";
  cropImage.src = "/static/assets/icons/soil.png";

  // Update fertility score
  fertilityScoreElement.textContent = result.fertility_score;
  const fertilityInfo = getFertilityInfo(result.fertility_score);
  fertilityCategoryElement.textContent = fertilityInfo.category;
  scoreImage.src = fertilityInfo.image;

  resultSection.classList.remove("hidden");
  resultSection.scrollIntoView({ behavior: "smooth" });
}

function getFertilityInfo(score) {
  return FERTILITY_CATEGORIES.find(category => 
    score >= category.min && score <= category.max
  ) || {
    category: "Unknown fertility level",
    image: "/static/assets/icons/fertilizer.png"
  };
}

function handleScroll() {
  const opacity = 1 - window.scrollY / 500;
  const newOpacity = Math.max(opacity, 0);
  backButton.style.opacity = newOpacity;
  infoButtonContainer.style.opacity = newOpacity;
}