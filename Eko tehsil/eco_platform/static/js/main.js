// Main javascript file
console.log("Ekoloji Platforma Yükləndi!");

// Audio System using Text-to-Speech (TTS)
const synth = window.speechSynthesis;

function playSound(type) {
    if (!synth) return;
    synth.cancel();

    let text = "";
    if (type === 'correct') {
        const phrases = ["Afərin!", "Əla!", "Düzgündür!", "Super!"];
        text = phrases[Math.floor(Math.random() * phrases.length)];
    } else if (type === 'wrong') {
        const phrases = ["Səhvdir", "Yenidən yoxla", "Təəssüf", "Bir daha cəhd et"];
        text = phrases[Math.floor(Math.random() * phrases.length)];
    }

    if (text) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.1;
        utterance.pitch = 1.2;
        synth.speak(utterance);
    }
}

async function saveScore(points) {
    try {
        const response = await fetch('/api/add_points', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ points: points })
        });
        const data = await response.json();
        console.log("New Score:", data.new_score);
    } catch (error) {
        console.error("Error saving score:", error);
    }
}

window.playSound = playSound;
window.saveScore = saveScore;
