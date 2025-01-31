const btn = document.querySelector('.talk');
const content = document.querySelector('.content');

function speak(text) {
  const text_speak = new SpeechSynthesisUtterance(text);
  text_speak.rate = 1;
  text_speak.volume = 1;
  text_speak.pitch = 1;

  window.speechSynthesis.speak(text_speak);
}

function wishMe() {
  let hour = new Date().getHours();
  if (hour >= 0 && hour < 12) {
    speak("Good Morning Sir!");
  } else if (hour >= 12 && hour < 18) {
    speak("Good Afternoon Sir!");
  } else {
    speak("Good Evening Sir!");
  }
}


window.addEventListener("load", () => {
  speak("Initializing ORION...");
  wishMe();
});

// Speech Recognition Setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (!SpeechRecognition) {
  content.textContent = "Speech Recognition not supported in this browser.";
  alert("Your browser does not support speech recognition. Use Google Chrome.");
} else {
  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  // When speech is detected
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript.toLowerCase();
    content.textContent = transcript; // Update UI
    takeCommand(transcript);
  };

  // If an error occurs
  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    content.textContent = "Error: " + event.error;
  };

  // When clicking the button
  btn.addEventListener('click', () => {
    content.textContent = "Listening...";
    recognition.start();
  });

  // Process the voice command
  function takeCommand(message) {
    if (message.includes('hello') || message.includes('hey')) {
      speak("Hello Sir, How May I Help You?");
    } else if (message.includes("open google")) {
      window.open("https://google.com", "_blank");
      speak("Opening Google...");
    } else if (message.includes("open youtube")) {
      window.open("https://youtube.com", "_blank");
      speak("Opening YouTube...");
    } else if (message.includes("open facebook")) {
      window.open("https://facebook.com", "_blank");
      speak("Opening Facebook...");
    } else if (message.includes('what is') || message.includes('who is') || message.includes('what are')) {
      window.open(`https://www.google.com/search?q=${message.replace(/ /g, "+")}`, "_blank");
      speak("This is what I found on the internet regarding " + message);
    } else if (message.includes('wikipedia')) {
      window.open(`https://en.wikipedia.org/wiki/${message.replace("wikipedia", "").trim()}`, "_blank");
      speak("This is what I found on Wikipedia regarding " + message);
    } else if (message.includes('time')) {
      const time = new Date().toLocaleTimeString();
      speak("The current time is " + time);
    } else if (message.includes('date')) {
      const date = new Date().toLocaleDateString();
      speak("Today's date is " + date);
    } else if (message.includes('calculator')) {
      window.open('https://www.calculator.net/', "_blank");
      speak("Opening Calculator");
    } else {
      window.open(`https://www.google.com/search?q=${message.replace(/ /g, "+")}`, "_blank");
      speak("I found some information for " + message + " on Google");
    }
  }
}
