
// Analyze Candidates Button

document.getElementById("analyze-btn").addEventListener("click", async function () {

    const analyzeBtn = document.getElementById("analyze-btn");

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = "⏳ Finding Best Candidates...";

    // Get Job Description
    const jobDescription = document
        .getElementById("job-description")
        .value;

    

    // Send data to Flask
    const response = await fetch("http://127.0.0.1:5000/analyze", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            job_description: jobDescription,
        })

    });

    const data = await response.json();
    window.candidates = data;

    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = "🚀 Find Best Candidates";

    console.log(data);
    document.getElementById("download-btn").style.display = "block";

    // Display Results
    const resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "<h2>Top Candidates</h2>";

data.forEach((candidate, index) => {

    resultsDiv.innerHTML += `
        <div class="result-card" onclick="showProfile(${index})">
            <h3>${candidate.candidate_id}</h3>
            <p>Match: ${(candidate.score * 100).toFixed(2)}%</p>
        </div>
    `;

});


});

document.getElementById("download-btn").addEventListener("click", () => {
    const link = document.createElement("a");
    link.href = "http://127.0.0.1:5000/download";
    link.download = "Top_Candidates.xlsx";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

function showProfile(index) {

    const candidate = window.candidates[index].candidate;

    const currentJob = candidate.career_history?.[0] || {};

    document.getElementById("profile-content").innerHTML = `
        <h2>${candidate.candidate_id}</h2>

        <p><b>Current Role:</b> ${currentJob.title || "N/A"}</p>

        <p><b>Company:</b> ${currentJob.company || "N/A"}</p>

        <p><b>Industry:</b> ${currentJob.industry || "N/A"}</p>

        <p><b>Experience:</b> ${currentJob.duration_months || "N/A"} months</p>

        <p><b>Description:</b></p>

        <div class="profile-box">
            ${currentJob.description || "No description available"}
        </div>

        <br>

        <details>
            <summary>📄 View Complete Profile</summary>

            <pre>${JSON.stringify(candidate, null, 2)}</pre>

        </details>
    `;

    document.getElementById("profile-modal").style.display = "block";
}

document.getElementById("close-modal").onclick = function () {
    document.getElementById("profile-modal").style.display = "none";
};