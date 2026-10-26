const canvas = document.getElementById("rede");
const ctx = canvas.getContext("2d");
let pontos = [];

function ajustarTamanho() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}

function criarPontos() {
    pontos = [];
    const quantidade = Math.floor((canvas.width * canvas.height) / 12000);

    for (let i = 0; i < quantidade; i++) {
        pontos.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5
        });
    }
}

function desenhar() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (const p of pontos) {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

        ctx.fillStyle = "rgba(139, 139, 254, 0.8)";
        ctx.beginPath();
        ctx.arc(p.x, p.y, 1.5, 0, Math.PI * 2);
        ctx.fill();
    }

    for (let i = 0; i < pontos.length; i++) {
        for (let j = i + 1; j < pontos.length; j++) {
            const dx = pontos[i].x - pontos[j].x;
            const dy = pontos[i].y - pontos[j].y;
            const distancia = Math.sqrt(dx * dx + dy * dy);

            if (distancia < 120) {
                ctx.strokeStyle = `rgba(65, 65, 252, ${1 - distancia / 120})`;
                ctx.lineWidth = 0.6;
                ctx.beginPath();
                ctx.moveTo(pontos[i].x, pontos[i].y);
                ctx.lineTo(pontos[j].x, pontos[j].y);
                ctx.stroke();
            }
        }
    }

    requestAnimationFrame(desenhar);
}

ajustarTamanho();
criarPontos();
desenhar();

window.addEventListener("resize", () => {
    ajustarTamanho();
    criarPontos();
});