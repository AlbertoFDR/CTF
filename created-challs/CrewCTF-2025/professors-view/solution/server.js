const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const path = require("path");
const https = require("https");  
const http = require("http");  

const app = express();
const PORT = 443;

// generate ssl
// openssl req -x509 -nodes -days 365 -newkey rsa:2048  -keyout private-key.pem -out certificate.pem -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=example.com"
// SSL certificates (replace with your own paths if needed)
const privateKey = fs.readFileSync("private-key.pem", "utf8");
const certificate = fs.readFileSync("certificate.pem", "utf8");
const credentials = { key: privateKey, cert: certificate };

app.use(bodyParser.json({ limit: "10mb" })); // Increase limit to handle large images

app.get('/', (req, res) => {
    console.log(`[*] Request: ${req.originalUrl}`);
    res.sendFile(path.join(__dirname,'./index.html'));
});


app.post("/upload", (req, res) => {
    console.log("[X] Uploading screenshot");
    const { image } = req.body;

    if (!image) {
        return res.status(400).json({ message: "No image provided" });
    }

    // Decode Base64 to Buffer
    const base64Data = image.replace(/^data:image\/png;base64,/, "");
    const filePath = `screenshots/screenshot_${Date.now()}.png`;

    // Save to file
    fs.mkdirSync("screenshots", { recursive: true });
    fs.writeFile(filePath, base64Data, "base64", (err) => {
        if (err) {
            console.error("Error saving image:", err);
            return res.status(500).json({ message: "Failed to save image" });
        }
        res.json({ message: "Screenshot saved successfully!", path: filePath });
    });
});


app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
