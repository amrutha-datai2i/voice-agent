import streamlit as st

# HTML and JavaScript for audio recording
audio_recorder_html = """
<script>
async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    let chunks = [];

    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
    mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        chunks = [];
        const formData = new FormData();
        formData.append('file', blob, 'audio.wav');

        // Send the audio file to the backend
        const response = await fetch('http://<your-ec2-public-ip>:8000/upload-audio', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play();
        } else {
            alert('Error: ' + (await response.text()));
        }
    };

    mediaRecorder.start();
    setTimeout(() => mediaRecorder.stop(), 5000); // Record for 5 seconds
}
</script>

<button onclick="startRecording()">Record Audio</button>
"""

# Render the HTML/JS in Streamlit
st.title("Voice-Enabled ElevenLabs Assistant")
st.markdown("Click the button below to record a 5-second audio clip.")
st.components.v1.html(audio_recorder_html)