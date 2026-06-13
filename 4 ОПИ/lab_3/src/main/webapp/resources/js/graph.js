let svg;
let centerX = 210;
let centerY = 210;
let rPixels = 170; // -- кол-во пикселей на радиус
let RMax = 5;


function unit() {
    return rPixels / RMax;
}

function toX(x) {
    return centerX + unit() * x;
}

function toY(y) {
    return centerY - unit() * y;
}

function getCurrentR() {
    const el = document.getElementById("appForm:rValue");
    const v = parseFloat(el?.value);
    return v > 0 ? v : NaN;
}

function initGraph() {
    svg = document.getElementById("graphSvg");
    if (!svg) return;

    if (!svg.dataset.clickAdded) {
        svg.addEventListener("click", onGraphClick);
        svg.dataset.clickAdded = "1";
    }

    findMaxR();
}

function findMaxR() {
    let max = 0;
    document.querySelectorAll('#appForm\\:r input[type="radio"]').forEach(el => {
        const v = Math.abs(parseFloat(el.value));
        if (v > max) max = v;
    });

    RMax = max || 5;
}

function drawTicks() {
    const g = svg.querySelector("#ticks");
    if (!g) return;

    const R = getCurrentR();
    if (!R) {
        g.innerHTML = "";
        return;
    }

    let html = "";

    function tickX(x, label) {
        const px = toX(x);
        html += `
        <g>
            <line x1="${px}" y1="${centerY - 4}" x2="${px}" y2="${centerY + 4}" stroke="white"/>
            <text x="${px}" y="${centerY - 8}" fill="white" font-size="12" text-anchor="middle">${label}</text>
        </g>`;
    }

    function tickY(y, label) {
        const py = toY(y);
        html += `
        <g>
            <line x1="${centerX - 4}" y1="${py}" x2="${centerX + 4}" y2="${py}" stroke="white"/>
            <text x="${centerX + 6}" y="${py + 4}" fill="white" font-size="12">${label}</text>
        </g>`;
    }

    tickX(-R, "-R");
    tickX(-R / 2, "-R/2");
    tickX(R / 2, "R/2");
    tickX(R, "R");

    tickY(R, "R");
    tickY(R / 2, "R/2");
    tickY(-R / 2, "-R/2");
    tickY(-R, "-R");

    g.innerHTML = html;
}

function drawArea() {
    const g = svg.querySelector("#area");
    if (!g) return;

    const R = getCurrentR();
    if (!R) {
        g.innerHTML = "";
        return;
    }

    let d = "";

    const p = [
        [toX(-R), toY(0)],
        [toX(0), toY(0)],
        [toX(0), toY(-R)],
        [toX(-R), toY(-R)]
    ];
    d += `M ${p[0]} L ${p[1]} L ${p[2]} L ${p[3]} Z`;

    const t = [
        [toX(-R), toY(0)],
        [toX(0), toY(R / 2)],
        [toX(0), toY(0)]
    ];
    d += ` M ${t[0]} L ${t[1]} L ${t[2]} Z`;

    const rad = R / 2;
    const radPx = unit() * rad;

    const arcStart = [toX(rad), toY(0)];
    const arcEnd = [toX(0), toY(-rad)];

    d += ` M ${centerX} ${centerY}
           L ${arcStart}
           A ${radPx} ${radPx} 0 0 1 ${arcEnd}
           Z`;

    g.innerHTML = `<path d="${d}" fill="#8cc3ff" fill-opacity="0.45" stroke="white"></path>`;
}

function positionPoints() {
    const R = getCurrentR();
    const hide = !R;

    svg.querySelectorAll("#pointsLayer circle").forEach(el => {
        if (hide) {
            el.setAttribute("visibility", "hidden");
            return;
        }

        const x = parseFloat(el.dataset.x);
        const y = parseFloat(el.dataset.y);
        const r0 = parseFloat(el.dataset.r);

        const xx = x * (R / r0);
        const yy = y * (R / r0);

        el.setAttribute("visibility", "visible");
        el.setAttribute("cx", toX(xx));
        el.setAttribute("cy", toY(yy));
    });
}

function onGraphClick(e) {
    const R = getCurrentR();
    if (!R) return;

    const rect = svg.getBoundingClientRect();
    const px = e.clientX - rect.left;
    const py = e.clientY - rect.top;

    const x = (px - centerX) / unit();
    const y = (centerY - py) / unit();

    if (y < -5 || y > 3) {
        showGraphError("Ошибка", "Y должен быть в диапазоне [-5; 3]");
        return;
    }

    rcSendPoint([
        { name: "x", value: x.toFixed(6) },
        { name: "y", value: y.toFixed(6) }
    ]);
}

function showGraphError(title, text) {
    const block = document.getElementById("graphErrorDisplay");
    if (!block) return;

    block.textContent = `${title}: ${text}`;
    block.style.display = "block";

    setTimeout(() => {
        block.style.display = "none";
    }, 4000);
}

function redrawAll() {
    initGraph();
    if (!svg) return;

    drawTicks();
    drawArea();
    positionPoints();
}

document.addEventListener("DOMContentLoaded", () => {
    initGraph();
    redrawAll();
});

window.redrawAll = redrawAll;
