/* ===== AABC ===== */

// JavaScript code to trigger the animation when the elements come into view
const animations = [
  { selector: ".card-insurance", threshold: 0.2 },
  { selector: ".wp-block-uagb-modal", threshold: 0.4 },
  { selector: ".title-underline", threshold: 0.2 },
];

const delay = 300; // Default delay value in milliseconds

animations.forEach((animation) => {
  const items = document.querySelectorAll(animation.selector);
  const options = {
    root: null,
    rootMargin: "0px",
    threshold: animation.threshold,
  };
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        const item = entry.target;
        setTimeout(() => {
          item.classList.add("visible");
        }, delay * index);
      }
    });
  }, options);
  items.forEach((item) => observer.observe(item));
});

// ----------------- CAROUSEL -----------------
const slider = document.querySelector(".slider");
const container = document.querySelector(".slide-track");
const slides = container.querySelectorAll(".slide");
const slideWidth = slides[0].clientWidth + 80;
let currentPosition = -slideWidth; // start at the second slide
let cloneCount = 0; // number of clones on each side

// Add loading="eager" to all the img tags
slides.forEach((slide) => {
  const img = slide.querySelector("img");
  img.setAttribute("loading", "eager");
});

// position the slides absolutely
container.style.position = "relative";
slides.forEach((slide, index) => {
  slide.style.position = "absolute";
  slide.style.left = index * slideWidth + "px";
});

// animate the slider
function animateSlider() {
  currentPosition += 3;
  slides.forEach((slide) => {
    let slidePosition = parseInt(slide.style.left, 10);
    slidePosition += 1;
    slide.style.left = slidePosition + "px";
    if (slidePosition > (slides.length - 1) * slideWidth) {
      slide.style.left =
        -slideWidth +
        (slidePosition - (slides.length - 1) * slideWidth) -
        2 * cloneCount * slideWidth +
        "px";
    }
  });
  animationId = requestAnimationFrame(animateSlider);
}
requestAnimationFrame(animateSlider);

slider.addEventListener("mouseenter", () => {
  cancelAnimationFrame(animationId); // pause the animation
});

slider.addEventListener("mouseleave", () => {
  animationId = requestAnimationFrame(animateSlider); // resume the animation
});
