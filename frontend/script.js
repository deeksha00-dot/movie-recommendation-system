async function getRecommendations() {

    const input = document.getElementById("movieInput");
    const message = document.getElementById("message");
    const resultTitle = document.getElementById("resultTitle");
    const recommendations = document.getElementById("recommendations");

    const movie = input.value.trim();

    if (!movie) {
        message.textContent = "Please enter a movie name.";
        return;
    }

    message.textContent = "Loading...";
    recommendations.innerHTML = "";
    resultTitle.textContent = "";

    try {

        const url =
            "http://127.0.0.1:8000/recommend/" +
            encodeURIComponent(movie);

        console.log("Requesting:", url);

        const response = await fetch(url);

        console.log("Status:", response.status);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Movie not found");
        }

        const data = await response.json();

        console.log("Response:", data);

        message.textContent = "";

        resultTitle.textContent =
            "Movies similar to " + data.movie;

        data.recommendations.forEach(movie => {

            const card = document.createElement("div");

            card.className = "movie-card";

            card.innerHTML = `
                <h3>${movie.title}</h3>
                <p>⭐ Rating: ${movie.rating}</p>
                <p>Release: ${movie.release_date || "Unknown"}</p>
                <p>${movie.overview || "No description available."}</p>
            `;

            recommendations.appendChild(card);
        });

    } catch (error) {

        console.error("Error:", error);

        message.textContent =
            "Movie not found. Try another movie.";
    }
}