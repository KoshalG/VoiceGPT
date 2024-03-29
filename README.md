# VoiceGPT
VoiceGPT is a web based voice assistant powered by ChatGPT
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CrowdStrike Falcon Reports</title>
    <!-- Include Astro Tailwind CSS -->
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 p-8">
    <div class="container mx-auto">
        <h1 class="text-2xl font-bold mb-4">CrowdStrike Falcon Reports</h1>
        <table class="table-auto">
            <thead>
                <tr>
                    <th class="px-4 py-2 bg-gray-200">ID</th>
                    <th class="px-4 py-2 bg-gray-200">Customer ID</th>
                    <th class="px-4 py-2 bg-gray-200">User ID</th>
                    <th class="px-4 py-2 bg-gray-200">Name</th>
                    <th class="px-4 py-2 bg-gray-200">Description</th>
                    <th class="px-4 py-2 bg-gray-200">Status</th>
                    <th class="px-4 py-2 bg-gray-200">Type</th>
                    <th class="px-4 py-2 bg-gray-200">Schedule</th>
                    <th class="px-4 py-2 bg-gray-200">Created On</th>
                    <th class="px-4 py-2 bg-gray-200">Last Updated On</th>
                </tr>
            </thead>
            <tbody id="reportTableBody">
                <!-- Table rows will be added dynamically here -->
            </tbody>
        </table>
    </div>

    <script>
        // Function to fetch data from JSON file and create table rows
        async function fetchDataAndCreateTable() {
            const response = await fetch('data/crowdstrikefalcon.json');
            const data = await response.json();

            const tableBody = document.getElementById('reportTableBody');
            data.forEach(entry => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="border px-4 py-2">${entry.id}</td>
                    <td class="border px-4 py-2">${entry.customer_id}</td>
                    <td class="border px-4 py-2">${entry.user_id}</td>
                    <td class="border px-4 py-2">${entry.name}</td>
                    <td class="border px-4 py-2">${entry.description}</td>
                    <td class="border px-4 py-2">${entry.status}</td>
                    <td class="border px-4 py-2">${entry.type}</td>
                    <td class="border px-4 py-2">${entry.schedule.display}</td>
                    <td class="border px-4 py-2">${entry.created_on}</td>
                    <td class="border px-4 py-2">${entry.last_updated_on}</td>
                `;
                tableBody.appendChild(row);
            });
        }

        // Call the function to fetch data and create table rows
        fetchDataAndCreateTable();
    </script>
</body>
</html>
