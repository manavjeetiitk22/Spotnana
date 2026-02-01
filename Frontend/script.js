const form = document.getElementById("searchForm");
const resultsDiv = document.getElementById("results");

const API_BASE =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "http://backend:8000";

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const origin = document.getElementById("origin").value.toUpperCase();
    const destination = document.getElementById("destination").value.toUpperCase();
    const date = document.getElementById("date").value;

    resultsDiv.innerHTML = "<p>Searching...</p>";

    try {
        const response = await fetch(
            `${API_BASE}/search?origin=${origin}&destination=${destination}&date=${date}`
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

        const flights = itinerary.flights;

        // ---- Route ----
        const route =
            flights.map(f => f.origin).join(" → ") +
            " → " +
            flights[flights.length - 1].destination;

        // ---- Total travel time ----
        const start = new Date(flights[0].departureTime);
        const end = new Date(flights[flights.length - 1].arrivalTime);
        const totalMinutes = Math.floor((end - start) / 60000);

        const totalHours = Math.floor(totalMinutes / 60);
        const totalMins = totalMinutes % 60;

        let html = `
            <h3>Itinerary ${idx + 1} (${flights.length - 1} stops)</h3>
            <p><strong>Route:</strong> ${route}</p>
            <p><strong>Total travel time:</strong> ${totalHours}h ${totalMins}m</p>
            <pre>
        `;

        flights.forEach((flight, i) => {
            html += `${flight.flightNumber} | ${flight.origin} → ${flight.destination} | $${flight.price}\n`;
            html += `  ${flight.departureTime} → ${flight.arrivalTime}\n`;

            if (itinerary.layovers && i < itinerary.layovers.length) {
                const layover = itinerary.layovers[i];
                html += `  Layover at ${layover.airport}: ${layover.duration_human}\n`;
            }
        });

        html += `\nTotal price: $${itinerary.total_price}`;
        html += `</pre>`;

        div.innerHTML = html;
        resultsDiv.appendChild(div);
    });
}

