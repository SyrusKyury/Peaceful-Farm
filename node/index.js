const express = require('express');
const fs = require('fs');
const { execSync } = require('child_process');
const app = express();
const port = 8000;

// Middleware to parse the body of the request
app.use(express.json());

app.post('/', (req, res) => {

    // Check if the body contains the 'code' field
    if (!req.body || !req.body.code) {
        return res.status(400).send({
            message: "Content can not be empty!"
        });
    }

    const code = req.body.code;
    // Generate the filename for the temporary file
    const filename = `temp-${Date.now()}.js`;
    const filePath = `/tmp/${filename}`;

    try {
        // Write the code to the temporary file
        fs.writeFileSync(filePath, code);

        // Execute the code and capture the output
        const output = execSync(`node ${filePath}`).toString();
        
        // Send the output back as a JSON response
        res.json({ 'output': output });
    } catch (err) {
        // Handle errors if something goes wrong
        res.status(500).send({ message: "An error occurred", error: err.message });
    } finally {
        // Clean up the temporary file (optional, for security)
        if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
        }
    }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
