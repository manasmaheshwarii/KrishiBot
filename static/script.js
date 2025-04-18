document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("file-input");
  const dropArea = document.getElementById("drop-area");
  const browseBtn = document.getElementById("browse-btn");
  const uploadBtn = document.getElementById("upload-btn");
  const preview = document.getElementById("preview");
  const loader = document.getElementById("loader");

  const plantName = document.getElementById("plant-name");
  const diseaseName = document.getElementById("disease-name");
  const solutionText = document.getElementById("solution-text");
  const predictionSection = document.getElementById("prediction-result");

  let selectedFile;

  function handleFile(file) {
    if (file) {
      selectedFile = file;
      document.getElementById(
        "file-name"
      ).textContent = `Selected File: ${file.name}`;
      const reader = new FileReader();
      reader.onload = (e) => {
        preview.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image">`;
      };
      reader.readAsDataURL(file);
    }
  }

  dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("drag-over");
  });

  dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("drag-over");
  });

  dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("drag-over");
    const file = e.dataTransfer.files[0];
    fileInput.files = e.dataTransfer.files;
    handleFile(file);
  });

  browseBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    fileInput.click();
  });

  fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    handleFile(file);
  });

  uploadBtn.addEventListener("click", async () => {
    if (!selectedFile) {
      alert("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    loader.classList.remove("hidden");

    try {
      const response = await fetch("/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      loader.classList.add("hidden");

      if (data.error) {
        alert(data.error);
        return;
      }

      plantName.textContent = data.plant || "N/A";
      diseaseName.textContent = data.disease || "N/A";
      solutionText.textContent = data.solution || "N/A";

      predictionSection.classList.remove("hidden");

      // Chart.js donut chart
      const ctx = document.getElementById("confidenceChart").getContext("2d");
      new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: ["Confidence", "Unsure"],
          datasets: [
            {
              label: "",
              data: [
                100 - parseFloat(data.confidence),
                parseFloat(data.confidence),
              ],
              backgroundColor: ["#1e5128", "#d3e8d1"],
              borderWidth: 1,
            },
          ],
        },
        options: {
          cutout: "70%",
          plugins: {
            legend: { display: false },
            tooltip: { enabled: true },
          },
        },
      });
    } catch (error) {
      loader.classList.add("hidden");
      alert("Error uploading image.");
      console.error(error);
    }
  });
});
