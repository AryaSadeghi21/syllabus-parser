// Global error handler to prevent page reloads
window.addEventListener("error", function (e) {
  console.error("Global error caught:", e.error);
  e.preventDefault();
  return false;
});

window.addEventListener("unhandledrejection", function (e) {
  console.error("Unhandled promise rejection:", e.reason);
  e.preventDefault();
  return false;
});

// Prevent any form submission
document.addEventListener("submit", function (e) {
  console.log("Form submission prevented");
  e.preventDefault();
  return false;
});

// Prevent any button clicks from causing page reload
document.addEventListener("click", function (e) {
  if (e.target.tagName === "BUTTON" && e.target.type !== "button") {
    e.preventDefault();
  }
});

// DOM Elements
const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const selectedFile = document.getElementById("selectedFile");
const fileName = document.getElementById("fileName");
const fileSize = document.getElementById("fileSize");
const processBtn = document.getElementById("processBtn");
const status = document.getElementById("status");
const statusText = document.getElementById("statusText");
const progressFill = document.getElementById("progressFill");
const exportOptions = document.getElementById("exportOptions");
const n8nBtn = document.getElementById("n8nBtn");

let selectedFileData = null;
let semesterStartDate = null;

// Semester date input
const semesterStartDateInput = document.getElementById("semesterStartDate");

// Initialize with no default date
semesterStartDate = null;

// Update semester date when user changes it
semesterStartDateInput.addEventListener("change", (e) => {
  semesterStartDate = e.target.value;
});

// Drag and drop functionality
uploadArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadArea.classList.add("dragover");
});

uploadArea.addEventListener("dragleave", () => {
  uploadArea.classList.remove("dragover");
});

uploadArea.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadArea.classList.remove("dragover");
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    handleFile(files[0]);
  }
});

// Remove the click handler from upload area since file input will handle it directly

fileInput.addEventListener("change", (e) => {
  console.log("File input changed", e.target.files);
  if (e.target.files.length > 0) {
    handleFile(e.target.files[0]);
  }
  // Clear the input value to prevent issues with re-selecting the same file
  e.target.value = "";
});

function handleFile(file) {
  if (file.type !== "application/pdf") {
    alert("Please select a PDF file.");
    return;
  }

  selectedFileData = file;
  fileName.textContent = file.name;
  fileSize.textContent = formatFileSize(file.size);
  selectedFile.style.display = "block";
  processBtn.style.display = "inline-block";
  exportOptions.style.display = "none";
  status.style.display = "none";
}

function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

async function sendPdfToN8n(pdfFile, semesterStartDate) {
  try {
    console.log("Starting PDF to n8n process...");

    // First, extract text from PDF using backend
    const textFormData = new FormData();
    textFormData.append("file", pdfFile);

    console.log("Extracting text from PDF...");
    console.log("Backend URL:", "http://localhost:8000/api/extract-text");

    const textResponse = await fetch("http://localhost:8000/api/extract-text", {
      method: "POST",
      body: textFormData,
    });

    console.log("Text extraction response status:", textResponse.status);

    if (!textResponse.ok) {
      const errorText = await textResponse.text();
      console.error("Text extraction failed:", errorText);
      throw new Error(
        `Failed to extract text from PDF: ${textResponse.status} - ${errorText}`
      );
    }

    const textData = await textResponse.json();
    console.log("PDF text extracted:", {
      totalPages: textData.total_pages,
      textLength: textData.extracted_text.length,
    });

    // Now send PDF, text, and date to n8n
    const n8nFormData = new FormData();
    n8nFormData.append("file", pdfFile); // Original PDF
    n8nFormData.append("semester_start_date", semesterStartDate || "");
    n8nFormData.append("extracted_text", textData.extracted_text);
    n8nFormData.append("total_pages", textData.total_pages.toString());
    n8nFormData.append("file_name", pdfFile.name);

    console.log("Sending to n8n:", {
      fileName: pdfFile.name,
      fileSize: pdfFile.size,
      semesterStartDate: semesterStartDate,
      textLength: textData.extracted_text.length,
    });

    const response = await fetch(
      "https://n8n.srv902180.hstgr.cloud/webhook-test/syllabus-input",
      {
        method: "POST",
        body: n8nFormData,
      }
    );

    console.log("n8n response status:", response.status);
    console.log("n8n response headers:", response.headers);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("n8n request failed:", errorText);
      throw new Error(
        `Failed to send data to n8n: ${response.status} - ${errorText}`
      );
    }

    const result = await response.text();
    console.log("n8n response:", result);
    return result;
  } catch (error) {
    console.error("n8n send error:", error);
    throw error;
  }
}

processBtn.addEventListener("click", async (e) => {
  e.preventDefault(); // Prevent any default form submission
  if (!selectedFileData) return;

  try {
    // Show processing state
    processBtn.disabled = true;
    processBtn.innerHTML = '<span class="spinner"></span> Processing...';
    status.style.display = "block";
    status.className = "status processing";
    statusText.innerHTML =
      '<span class="spinner"></span> Extracting text from PDF...';

    // Simulate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
      progress += Math.random() * 15;
      if (progress > 90) progress = 90;
      progressFill.style.width = progress + "%";
    }, 200);

    // Send PDF directly to n8n with semester start date
    await sendPdfToN8n(selectedFileData, semesterStartDate);

    // Complete progress
    clearInterval(progressInterval);
    progressFill.style.width = "100%";

    // Show success
    status.className = "status success";
    statusText.textContent =
      "✅ PDF text extracted and sent to n8n successfully!";
    processBtn.style.display = "none";
    exportOptions.style.display = "block";
  } catch (error) {
    console.error("Error sending to n8n:", error);
    status.className = "status error";
    statusText.textContent = `❌ Error sending to n8n: ${error.message}`;
    processBtn.disabled = false;
    processBtn.textContent = "Process Syllabus";

    // Keep error message visible for 10 seconds
    setTimeout(() => {
      status.style.display = "none";
    }, 10000);
  }
});

n8nBtn.addEventListener("click", async () => {
  if (!selectedFileData) {
    alert("No file available. Please upload a PDF first.");
    return;
  }

  try {
    n8nBtn.disabled = true;
    n8nBtn.innerHTML = "<span class='spinner'></span> Exporting...";

    await sendPdfToN8n(selectedFileData, semesterStartDate);

    alert(
      "✅ PDF exported successfully! You can now use this file in your n8n automation."
    );
  } catch (error) {
    console.error("n8n export error:", error);
    alert(`❌ Error exporting PDF: ${error.message}`);
  } finally {
    n8nBtn.disabled = false;
    n8nBtn.innerHTML = "🔄 Export to n8n";
  }
});
