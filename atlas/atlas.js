const modal = {
    self: new bootstrap.Modal(document.getElementById('windowCountry')),
    title: document.getElementById('modalHeader'),
    body: document.getElementById('modalBody'),
    maps: document.getElementById('google-maps-link')
};
const continents = [
    document.getElementById('europe'),
    document.getElementById('asia'),
    document.getElementById('africa'),
    document.getElementById('americas'),
    document.getElementById('oceania'),
    document.getElementById('antarctic')
];

function formatNumber(num) {
    let formatted = '';
    for (let i = 0; i < String(num).length; i++) {
        if (i > 0 && (String(num).length - i) % 3 === 0) {
            formatted += '&nbsp;';
        }
        formatted += String(num)[i];
    }
    return formatted;
}

async function getData(region) {
    const url = `https://restcountries.com/v3.1/region/${region}`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const json = await response.json();
        let blocks = '';
        json.forEach((country) => {
            if (country.capital === undefined) {
                country.capital = 'N/A';
            }

            blocks += `
            <div class="col-xl-2 col-lg-3 col-md-4 col-sm-6 p-3 m-0">
                <div class="card border-2">
                    <img class="card-img-top" src="${country.flags.png}" alt="Vlajka">
                    <div class="card-body">
                        <h4 class="card-title">${country.name.common} (${country.cca3})</h4>
                    </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item"><b>Capital:</b> ${country.capital}</li>
                    </ul>
                    <div class="card-body">
                        <a href="#" class="btn btn-dark card-link" data-name="${country.name.common}">Learn more</a>
                    </div>
                </div>
            </div>
            `;
        });
        listCountries.innerHTML = blocks;

        document.querySelectorAll('[data-name]').forEach((button) => {
            button.addEventListener('click', () => {
                const countryName = button.getAttribute('data-name');
                modal.self.show()
                fetch(`https://restcountries.com/v3.1/name/${countryName}`)
                    .then((res) => res.json())
                    .then((data) => {
                        const country = data[0];
                        if (country.capital === undefined) {
                            country.capital = 'N/A';
                        }
                        if (country.subregion === undefined) {
                            country.subregion = 'N/A';
                        }
                        if (country.languages === undefined) {
                            country.languages = { 'N/A': 'N/A' };
                        }
                        if (country.currencies === undefined) {
                            country.currencies = { 'N/A': { name: 'N/A', symbol: 'N/A' } };
                        }

                        modal.title.innerHTML = `${country.name.common} (${country.cca3})`;
                        modal.body.innerHTML = `
                            <ul>
                                <li><b>Capital:</b> ${country.capital}</li>
                                <li><b>Population:</b> ${formatNumber(country.population)}</li>
                                <li><b>Area:</b> ${formatNumber(country.area)} km²</li>
                                <li><b>Subregion:</b> ${country.subregion}</li>
                                <li><b>Language${Object.values(country.languages).length > 1 ? 's' : ''}:</b> ${Object.values(country.languages).join(', ')}</li>
                                <li><b>Currency:</b> ${Object.values(country.currencies)[0].name} (${Object.values(country.currencies)[0].symbol})</li>
                            </ul>
                        `;
                        modal.maps.attributes.href.value = `${country.maps.googleMaps}`;
                    })
                    .catch((err) => {
                        console.error(err);
                        modal.body.innerHTML = `<p>Error while loading the information about the country.</p>`;
                    });
            });
        });
    } catch (error) {
        console.error(error.message);
    }
}

for (const continent of continents) {
    continent.addEventListener('click', () => {
        for (const element of continents) {
            element.classList.remove('border-bottom');
            element.classList.remove('disabled');
            element.classList.add('active');
        }

        continent.classList.remove('active');
        continent.classList.add('border-bottom');
        continent.classList.add('disabled');

        getData(continent.id);
    });
}

getData('europe');
