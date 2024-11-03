document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    // Clear previous status and result
    document.getElementById("uploadStatus").textContent = "Uploading...";
    document.getElementById("uploadedFile").textContent = "";
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
        const taskId = result.task_id;

        // Update status and show uploaded file name
        document.getElementById("uploadStatus").textContent = "File uploaded successfully! Generating document...";
        document.getElementById("uploadedFile").textContent = pdfFile.name;

        // Start polling for the task completion
        await pollForTaskCompletion(taskId);
        
    } catch (error) {
        document.getElementById("uploadStatus").textContent = `Error: ${error.message}`;
    }
});

// Function to poll for the task completion
async function pollForTaskCompletion(taskId) {
    const downloadLink = document.getElementById("downloadLink");
    const maxRetries = 9000000000;
    let retries = 0;

    while (retries < maxRetries) {
        try {
            // Check the task status
            const response = await fetch(`/task_status/${taskId}`);
            if (!response.ok) throw new Error("Failed to fetch task status");

            const result = await response.json();
            
            if (result.status === "completed") {
                // Task is complete, show download link
                document.getElementById("uploadStatus").textContent = "File ready for download!";
                downloadLink.href = `/static/output/${result.output_file}`;
                downloadLink.style.display = "block";
                return;
            } else if (result.status === "failed") {
                document.getElementById("uploadStatus").textContent = `Error: ${result.error}`;
                return;
            }
        } catch (error) {
            // Ignore errors and retry
        }

        // Wait for 2 seconds before retrying
        await new Promise(resolve => setTimeout(resolve, 2000));
        retries++;
    }

    // If max retries reached, show timeout message
    document.getElementById("uploadStatus").textContent = "File generation timed out. Please try again later.";
}