async function loadData() {
    const response = await fetch('tickets.csv');
    const data = await response.text();
 
    const rows = data.split('\n').slice(1);
 
    let counts = {
        MISSING: 0,
        DUPLICATE: 0,
        MISMATCH: 0,
        INVALID: 0
    };
 
    let tableHTML = "<tr><th>Issue</th><th>Event ID</th><th>Root Cause</th><th>Suggestion</th><th>Description</th></tr>";
 
    rows.forEach(row => {
        if (!row) return;
 
        let cols = row.split(',');
 
        let issue = cols[1];
        let event_id = cols[2];
        let root = cols[6];
        let suggestion = cols[7];
        let description = cols[4];
 
        if (counts[issue] !== undefined) {
            counts[issue]++;
        }
 
        tableHTML += `<tr>
            <td>${issue}</td>
            <td>${event_id}</td>
            <td>${root}</td>
            <td>${suggestion}</td>
            <td>${description}</td>
        </tr>`;
    });
 
    document.getElementById("dataTable").innerHTML = tableHTML;
 
    // Summary Cards
    document.getElementById("summary").innerHTML = `
        <div class="card"><h2>${counts.MISSING}</h2><p>Missing</p></div>
        <div class="card"><h2>${counts.DUPLICATE}</h2><p>Duplicate</p></div>
        <div class="card"><h2>${counts.MISMATCH}</h2><p>Mismatch</p></div>
        <div class="card"><h2>${counts.INVALID}</h2><p>Invalid</p></div>
    `;
 
    // Chart
    const ctx = document.getElementById('issueChart');
 
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Missing', 'Duplicate', 'Mismatch', 'Invalid'],
            datasets: [{
                label: 'Issue Count',
                data: [
                    counts.MISSING,
                    counts.DUPLICATE,
                    counts.MISMATCH,
                    counts.INVALID
                ]
            }]
        }
    });
}
 
loadData();