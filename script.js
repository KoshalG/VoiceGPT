const recordBtn = document.getElementById("record-btn"); // HTML button
const statusElement = document.querySelector(".status"); // HTML div
let recorder = null;
let isRecording = false;
let isProcessing = false;

recordBtn.addEventListener("click", async () => {
  // If we are already recording, stop it
  if (!isRecording) {
    isRecording = true;
    isProcessing = false;
    statusElement.innerHTML = "Audio being recorded";

    // Start recording
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      recorder = new MediaRecorder(stream, { mimeType: "audio/webm" });

      const chunks = [];
      recorder.addEventListener("dataavailable", (event) => {
        chunks.push(event.data);
      });

      recorder.start();

      let silenceTimeout = null;
      recorder.addEventListener("start", () => {
        silenceTimeout = setTimeout(() => {
          recorder.stop();
        }, 5000);
      });

      recorder.addEventListener("stop", () => {
        clearTimeout(silenceTimeout);

        const blob = new Blob(chunks, { type: "audio/webm" });
        sendAudio(blob);
      });
    } catch (error) {
      console.error(error);
      statusElement.innerHTML = "Failed to start recording";
      isRecording = false;
      isProcessing = false;
    }
  }
});

// Send audio to server
function sendAudio(blob) {
  statusElement.innerHTML = "Processing";
  fetch("/transcribe", {
    method: "POST",
    body: blob,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }
      return response.blob();
    })
    .then((audioBlob) => {
      playAudio(audioBlob);
      statusElement.innerHTML = "Playing audio";
    })
    .catch((error) => {
      console.error(error);
      statusElement.innerHTML = "Failed to process audio";
      isRecording = false;
      isProcessing = false;
    });
}

// Play audio
function playAudio(blob) {
  const audio = new Audio(URL.createObjectURL(blob));
  audio.addEventListener("ended", () => {
    statusElement.innerHTML = "Click the button to start recording";
    isRecording = false;
    isProcessing = false;
  });

  audio.play();
}
