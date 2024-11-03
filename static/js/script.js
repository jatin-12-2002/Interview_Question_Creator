document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    // Clear previous status and result
    document.getElementById("uploadStatus").textContent = "Uploading...";
    document.getElementById("uploadedFile").textContent = "Uploaded File";
    document.getElementById("downloadLink").style.display = "none";

    const formData = new FormData();
    const pdfFile = document.getElementById("pdfFile").files[0];
    const numQuestions = document.getElementById("numQuestions").value;

    // Ensure pdfFile and numQuestions are present
    if (!pdfFile || !numQuestions) {
        document.getElementById("uploadStatus").textContent = "Please upload a file and enter the number of questions.";
        return;
    }

    // Append form data
    formData.append("pdf_file", pdfFile);
    formData.append("num_questions", numQuestions);

    try {
        // Send form data to FastAPI backend
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const result = await response.json();
        
        // Update status and show uploaded file name
        document.getElementById("uploadStatus").textContent = "File uploaded successfully!";
        document.getElementById("uploadedFile").textContent = pdfFile.name;

        // Show download link for generated file
        const downloadLink = document.getElementById("downloadLink");
        downloadLink.href = `/static/output/${result.output_file}`;
        downloadLink.style.display = "block";
    } catch (error) {
        document.getElementById("uploadStatus").textContent = `Error: ${error.message}`;
    }
});