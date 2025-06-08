const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

const BASE_DIR = path.join(__dirname, "..", "chromadb", "model_output");

app.use(express.static(path.join(__dirname, "public")));
app.use("/machines", express.static(BASE_DIR));

app.get("/api/machines", (req, res) => {
    fs.readdir(BASE_DIR, { withFileTypes: true }, (err, files) => {
        if (err) {
            console.error("Failed to read model_output directory:", err);
            return res.status(500).json({ error: "Failed to read directories" });
        }

        const dirs = files
            .filter(f => f.isDirectory())
            .map(f => `machines/${f.name}`);

        res.json(dirs);
    });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});