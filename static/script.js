
let objectChart;
let dangerChart;

function dangerToScore(danger) {
    if (danger === "CRITICAL") return 95;
    if (danger === "WARNING") return 55;
    return 10;
}

function getDangerClass(danger) {
    if (danger === "CRITICAL") return "critical-text";
    if (danger === "WARNING") return "warning-text";
    return "safe-text";
}

function createCharts() {
    const objectCtx = document.getElementById("objectChart");

    objectChart = new Chart(objectCtx, {
        type: "doughnut",
        data: {
            labels: ["Person", "Chair", "Car", "Bottle", "Backpack", "Phone", "Bench", "Couch"],
            datasets: [{
                data: [1, 1, 1, 1, 1, 1, 1, 1],
                backgroundColor: [
                    "#00d9ff",
                    "#ffb703",
                    "#35e38b",
                    "#ff3b4f",
                    "#7c3aed",
                    "#38bdf8",
                    "#f97316",
                    "#22c55e"
                ],
                borderWidth: 0
            }]
        },
        options: {
            plugins: {
                legend: {
                    labels: {
                        color: "#eaf7ff"
                    }
                }
            }
        }
    });

    const dangerCtx = document.getElementById("dangerChart");

    dangerChart = new Chart(dangerCtx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Danger Score",
                data: [],
                borderColor: "#ffb703",
                backgroundColor: "rgba(255,183,3,0.25)",
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            scales: {
                x: {
                    ticks: { color: "#9fb3c8" },
                    grid: { color: "rgba(0,217,255,0.08)" }
                },
                y: {
                    min: 0,
                    max: 100,
                    ticks: { color: "#9fb3c8" },
                    grid: { color: "rgba(0,217,255,0.08)" }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#eaf7ff"
                    }
                }
            }
        }
    });
}

async function loadData() {
    try {
        const response = await fetch("/data");
        const data = await response.json();

        document.getElementById("object").innerText = data.object;
        document.getElementById("danger").innerText = data.danger;
        document.getElementById("direction").innerText = data.direction;
        document.getElementById("decision").innerText = data.decision;

        document.getElementById("live-decision").innerText =
            "NAVIGATION: " + data.decision;

        document.getElementById("left").innerText = data.left_status;
        document.getElementById("front").innerText = data.front_status;
        document.getElementById("right").innerText = data.right_status;

        const dangerElement = document.getElementById("danger");
        dangerElement.className = getDangerClass(data.danger);

        updateObjectChart(data.stats);
        updateDangerTimeline(data.timeline);
        updateHistory(data.history);
        updateDecisionLog(data.history);

    } catch (error) {
        console.log("Dashboard update error:", error);
    }
}

function updateObjectChart(stats) {
    if (!objectChart || !stats) return;

    objectChart.data.datasets[0].data = [
        stats.person || 0,
        stats.chair || 0,
        stats.car || 0,
        stats.bottle || 0,
        stats.backpack || 0,
        stats["cell phone"] || 0,
        stats.bench || 0,
        stats.couch || 0
    ];

    objectChart.update();
}

function updateDangerTimeline(timeline) {
    if (!dangerChart || !timeline) return;

    dangerChart.data.labels = timeline.map(item => item.time);
    dangerChart.data.datasets[0].data = timeline.map(item => item.danger_score);

    dangerChart.update();
}

function updateHistory(history) {
    const table = document.getElementById("history-body");
    table.innerHTML = "";

    if (!history || history.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="5">No detections yet</td>
            </tr>
        `;
        return;
    }

    history.forEach(item => {
        table.innerHTML += `
            <tr>
                <td>${item.time}</td>
                <td>${item.object}</td>
                <td class="${getDangerClass(item.danger)}">${item.danger}</td>
                <td>${item.direction}</td>
                <td>${item.decision}</td>
            </tr>
        `;
    });
}

function updateDecisionLog(history) {
    const log = document.getElementById("decision-log");
    log.innerHTML = "";

    if (!history || history.length === 0) {
        log.innerHTML = `
            <div class="log-item">
                <span>[INFO]</span> Waiting for AI detections...
            </div>
        `;
        return;
    }

    history.slice(0, 8).forEach(item => {
        log.innerHTML += `
            <div class="log-item">
                <span>[${item.danger}]</span>
                ${item.object} detected ${item.direction} → ${item.decision}
            </div>
        `;
    });
}

createCharts();
loadData();
setInterval(loadData, 1000);