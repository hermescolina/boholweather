document.addEventListener("DOMContentLoaded", () => {
    const boholTowns = [
        "Tagbilaran", "Alburquerque", "Alicia", "Anda", "Antequera", "Baclayon", 
        "Balilihan", "Batuan", "Bien Unido", "Bilar", "Buenavista", "Calape", 
        "Candijay", "Carmen", "Catigbian", "Clarin", "Corella", "Cortes", 
        "Dagohoy", "Danao", "Dauis", "Dimiao", "Duero", "Garcia Hernandez", 
        "Getafe", "Guindulman", "Inabanga", "Jagna", "Lila", "Loay", "Loboc", 
        "Loon", "Mabini", "Maribojoc", "Panglao", "Pilar", "Pres. Carlos P. Garcia", 
        "Sagbayan", "San Isidro", "San Miguel", "Sevilla", "Sierra Bullones", 
        "Sikatuna", "Talibon", "Trinidad", "Tubigon", "Ubay", "Valencia"
    ];

    const dataList = document.getElementById("cityList");
    const searchBtn = document.getElementById("searchBtn");
    const cityInput = document.getElementById("cityInput");

    if (!dataList || !searchBtn || !cityInput) {
        console.error("One or more essential elements not found!");
        return;
    }

    // ✅ Populate the dropdown list
    dataList.innerHTML = ""; 
    boholTowns.forEach(town => {
        const option = document.createElement("option");
        option.value = town;
        dataList.appendChild(option);
    });

    console.log("Dropdown options added successfully!"); 

    // ✅ Set default town to Loboc
    cityInput.value = "Loboc";
    fetchWeather("Loboc");

    // ✅ Handle the search button click event
    searchBtn.addEventListener("click", () => {
        const city = cityInput.value.trim();
        if (city) {
            fetchWeather(city);
        } else {
            alert("Please enter a city name");
        }
    });
});


async function fetchWeather(city) {
    try {
        const formattedCity = `${city}, Bohol, Philippines`; // ✅ Ensure correct location
        const response = await fetch(`https://api.weatherapi.com/v1/forecast.json?key=d445526a6ade42d8851230706241509&q=${encodeURIComponent(formattedCity)}&days=3`);
        
        if (!response.ok) throw new Error("City not found");
        
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        alert(error.message);
        console.error("Weather API error:", error);
    }
}


function updateUI(data) {
    document.getElementById("cityName").textContent = data.location.name;
    document.getElementById("weatherIcon").src = data.current.condition.icon;
    document.getElementById("temperature").textContent = `${data.current.temp_c}°C`;
    document.getElementById("weatherDescription").textContent = data.current.condition.text;

    const forecastContainer = document.getElementById("forecast");
    if (!forecastContainer) return;
    forecastContainer.innerHTML = ""; 

    data.forecast.forecastday.forEach(day => {
        const date = new Date(day.date);
        const formattedDate = `${date.getMonth() + 1}/${date.getDate()}`; 

        const forecastItem = document.createElement("div");
        forecastItem.classList.add("forecast-day");
        forecastItem.innerHTML = `
            <h3>${formattedDate}</h3>
            <img src="${day.day.condition.icon}" alt="Weather Icon">
            <p>${day.day.avgtemp_c}°C</p>
            <p>${day.day.condition.text}</p>
        `;
        forecastContainer.appendChild(forecastItem);
    });

    console.log(data.forecast.forecastday);
}
