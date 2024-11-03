// script.js

// Elements
const uploadForm = document.getElementById('uploadForm');
const pdfFileInput = document.getElementById('pdfFile');
const numQuestionsInput = document.getElementById('numQuestions');
const filePreview = document.getElementById('filePreview');
const fileName = document.getElementById('fileName');
const outputLink = document.getElementById('outputLink');
const downloadLink = document.getElementById('downloadLink');

// Display selected file name
pdfFileInput.addEventListener('change', () => {
  const file = pdfFileInput.files[0];
  if (file) {
    fileName.textContent = file.name;
    filePreview.style.display = 'block';
  } else {
    filePreview.style.display = 'none';
  }
});

// Form submission handler
uploadForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData();
  formData.append('pdf_file', pdfFileInput.files[0]);
  formData.append('num_questions', numQuestionsInput.value);

  try {
    // Post form data to backend with full URL for Codespaces compatibility
    const response = await fetch(`${window.location.origin}/analyze`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Error Response:', errorText);
      throw new Error('Failed to generate questions');
    }

    // Parse JSON response
    const result = await response.json();

    // Show download link
    downloadLink.href = `${window.location.origin}/download/${result.output_file.split('/').pop()}`;
    downloadLink.style.display = 'inline';
    outputLink.style.display = 'block';
  } catch (error) {
    console.error(error);
    alert('An error occurred while generating questions. Please try again.');
  }
});