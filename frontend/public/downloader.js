window.onload = async () => {
    const container = document.getElementById("systemOptions");
    try {
        const res = await fetch("/api/machines");
        const machines = await res.json();
        machines.forEach(machinePath => {
            const name = machinePath.split("/").pop();
            const label = document.createElement("label");
            label.innerHTML = `<input type="radio" name="system" value="${machinePath}"> ${name}<br>`;
            container.appendChild(label);
        });
    } catch (err) {
        container.innerHTML = "Error loading machines.";
        console.error("Failed to fetch machine list:", err);
    }
};

let lastReportGenerated = null;

function nextStep(step) {
    if (step === 2 && !document.querySelector('input[name="system"]:checked')) {
        alert("Please select a system.");
        return;
    }
    if (step === 3 && !document.querySelector('input[name="format"]:checked')) {
        alert("Please select a format.");
        return;
    }

    document.getElementById("step" + (step - 1)).classList.add("hidden");
    document.getElementById("step" + step).classList.remove("hidden");

    if (step === 3) {
        const lastReportHeader = document.getElementById("lastReportHeader");
        const lastReportDate = document.getElementById("lastReportDate");
        if (lastReportGenerated) {
            lastReportDate.textContent = lastReportGenerated;
            lastReportHeader.classList.remove("hidden");
        } else {
            lastReportHeader.classList.add("hidden");
        }
    }
}

function generateReport(shouldGenerate) {
    document.getElementById("step3").classList.add("hidden");
    if (shouldGenerate) {
        lastReportGenerated = new Date().toLocaleDateString();
        document.getElementById("step4").classList.remove("hidden");
        updateDownloadLink();
    } else {
        alert("No new report generated.");
        document.getElementById("step1").classList.remove("hidden");
    }
}

function updateDownloadLink() {
    const system = document.querySelector('input[name="system"]:checked').value;
    const format = document.querySelector('input[name="format"]:checked').value;
    const extension = format === "word" ? "docx" : "pdf";
    const filename = `${extension}_output.${extension}`;
    const filepath = `./${system}/${filename}`;

    const link = document.getElementById("downloadLink");
    link.href = filepath;
    link.download = filename;
}

function downloadReport() {
    setTimeout(() => {
        document.getElementById("step4").classList.add("hidden");
        document.getElementById("step1").classList.remove("hidden");
    }, 1000);
    return true;
}
