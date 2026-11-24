
const API_BASE_URL = "http://127.0.0.1:8000";

async function loadCustomers() {
    const customerCount = document.getElementById(
        "total-customers"
    );

    const customerStatus = document.getElementById(
        "customer-status"
    );

    customerCount.textContent = "--";
    customerStatus.textContent = "Loading customers...";

    try {
        const response = await fetch(
            `${API_BASE_URL}/db/users`
        );

        if (!response.ok) {
            throw new Error(
                `API returned HTTP ${response.status}`
            );
        }

        const data = await response.json();

        if (!Array.isArray(data.users)) {
            throw new Error("Unexpected API response");
        }

        customerCount.textContent = data.users.length;
        customerStatus.textContent = "Connected to FastAPI";

        console.log("Customers loaded:", data.users);

    } catch (error) {
        console.error("Failed to load customers:", error);

        customerCount.textContent = "--";
        customerStatus.textContent =
            "Unable to connect to API";
    }
}

document.addEventListener("DOMContentLoaded", loadCustomers);
