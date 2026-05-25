async function predictDisease() {

    const fileInput = document.getElementById("imageInput");

    if (fileInput.files.length === 0) {
        alert("Select image first");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("/predict", {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    document.getElementById("result").innerHTML =
        "Disease: " + result.disease +
        "<br>Confidence: " + result.confidence;
}