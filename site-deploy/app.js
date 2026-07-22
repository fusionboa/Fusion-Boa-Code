// FusionBoa Website — Interactive Features
// Cycling code demo in the hero section

const samples = [
  `# FusionBoa — Hello World

let name be "FusionBoa"
let version be "1.0.0"

print "Hello, " + name + "!"

define function factorial with n:
    if n <= 1:
        return 1
    return n * factorial(n - 1)

let result be factorial(5)
print "Factorial(5) = " + result`,

  `def factorial(n):
    if (n <= 1):
        return 1
    return (n * factorial((n - 1)))

name = 'FusionBoa'
result = factorial(5)
print('Hello, ' + name + '!')
print('Factorial(5) =', result)`,

  `function factorial(n) {
  if ((n <= 1)) {
    return 1;
  }
  return (n * factorial((n - 1)));
}

let name = 'FusionBoa';
let result = factorial(5);
console.log('Hello, ' + name + '!');
console.log('Factorial(5) =', result);`,

  `fn main() {
    let result = factorial(5);
    println!("Hello, FusionBoa!");
    println!("Factorial(5) = {}", result);
}

fn factorial(n: i32) -> i32 {
    if (n <= 1) {
        return 1;
    }
    return (n * factorial((n - 1)));
}`,

  `package main

import "fmt"

func main() {
    result := factorial(5)
    fmt.Println("Hello, FusionBoa!")
    fmt.Println("Factorial(5) =", result)
}

func factorial(n int) int {
    if (n <= 1) {
        return 1
    }
    return (n * factorial((n - 1)))
}`,

  `<!DOCTYPE HTML>
<html lang="en">
  <head>
    <title>FusionBoa App</title>
  </head>
  <body>
    <h1>Hello from FusionBoa</h1>
    <p>Generated from one .fusboa file</p>
  </body>
</html>`,

  `{
  "app": "FusionBoa",
  "version": "1.0.0",
  "targets": 23,
  "languages": {
    "programming": 15,
    "markup": 8
  }
}`
];

const labels = [
  ".fusboa (FusionBoa)",
  ".py (Python)",
  ".js (JavaScript)",
  ".rs (Rust)",
  ".go (Go)",
  ".html (HTML)",
  ".json (JSON)"
];

let currentIndex = 0;
const codeDisplay = document.getElementById("code-display");
const codeLabel = document.getElementById("code-label");

function updateCode() {
  if (!codeDisplay) return;
  
  // Fade out
  codeDisplay.style.opacity = "0";
  
  setTimeout(() => {
    currentIndex = (currentIndex + 1) % samples.length;
    codeDisplay.textContent = samples[currentIndex];
    if (codeLabel) {
      codeLabel.textContent = labels[currentIndex] || "";
    }
    // Fade in
    codeDisplay.style.opacity = "1";
  }, 300);
}

// Initial display
if (codeDisplay) {
  codeDisplay.textContent = samples[0];
  codeDisplay.style.transition = "opacity 0.3s ease";
  if (codeLabel) codeLabel.textContent = labels[0];
}

// Rotate every 4 seconds
setInterval(updateCode, 4000);

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
});

// Intersection Observer for scroll animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "1";
      entry.target.style.transform = "translateY(0)";
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll(".feature-card, .target-card").forEach(el => {
  el.style.opacity = "0";
  el.style.transform = "translateY(30px)";
  el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
  observer.observe(el);
});

console.log("FusionBoa website loaded!");
