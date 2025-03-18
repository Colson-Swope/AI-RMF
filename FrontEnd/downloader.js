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
        let lastReportHeader = document.getElementById("lastReportHeader");
        let lastReportDate = document.getElementById("lastReportDate");
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
    let system = document.querySelector('input[name="system"]:checked').value;
    let format = document.querySelector('input[name="format"]:checked').value;
    let extension = format === "word" ? "docx" : "pdf";
    //let filename = `${system}_report.${extension}`;
    let filename = `${extension}_output.${extension}`;
    let filepath = `../chromadb_test/model_output/output_RMF-Client01/${filename}`;
    
    let link = document.getElementById("downloadLink");
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