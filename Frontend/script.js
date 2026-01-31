const form = document.getElementById("searchForm");
const resultsDiv = document.getElementById("results");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const origin = document.getElementById("origin").value.toUpperCase();
    const destination = document.getElementById("destination").value.toUpperCase();
    const date = document.getElementById("date").value;

    resultsDiv.innerHTML = "<p>Searching...</p>";

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/search?origin=${origin}&destination=${destination}&date=${date}`
        );

        const data = await response.json();
        renderResults(data);

    } catch (err) {
        resultsDiv.innerHTML = "<p>Error fetching results</p>";
    }
});

function renderResults(itineraries) {
    if (itineraries.length === 0) {
        resultsDiv.innerHTML = "<p>No itineraries found.</p>";
        return;
    }

    resultsDiv.innerHTML = "";

    itineraries.forEach((itinerary, idx) => {
        const div = document.createElement("div");
        div.className = "itinerary";

        let html = `<h3>Itinerary ${idx + 1}</h3>`;
        html += `<p>Total Price: $${itinerary.total_price}</p>`;

        html += "<ul>";
        itinerary.flights.forEach(f => {
            html += `
                <li>
                    ${f.flightNumber}: ${f.origin} → ${f.destination}<br>
                    ${f.departureTime} → ${f.arrivalTime}
                </li>
            `;
        });
        html += "</ul>";

        div.innerHTML = html;
        resultsDiv.appendChild(div);
    });
}
