// script.js
const canvas = document.getElementById("waveCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let waves = [];
const waveCount = 5;

// Initialize waves
for (let i = 0; i < waveCount; i++) {
    waves.push({
        amplitude: Math.random() * 50 + 30, // Height of wave
        frequency: Math.random() * 0.01 + 0.005, // Speed of wave
        phase: Math.random() * Math.PI * 2, // Start position
        offset: i * 80 + 50, // Position on y-axis
        color: `rgba(255, 255, 255, ${0.1 + i * 0.05})`, // Semi-transparent white
    });
}

// Animate the waves
function drawWaves() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.lineWidth = 2;

    waves.forEach(wave => {
        ctx.beginPath();
        ctx.strokeStyle = wave.color;

        for (let x = 0; x < canvas.width; x++) {
            const y =
                wave.offset +
                Math.sin(x * wave.frequency + wave.phase) * wave.amplitude;
            ctx.lineTo(x, y);
        }

        ctx.stroke();

        // Update the wave's phase to create motion
        wave.phase += 0.02;
    });

    requestAnimationFrame(drawWaves);
}

// Adjust canvas size on resize
window.addEventListener("resize", () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

drawWaves();
