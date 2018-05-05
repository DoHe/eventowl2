const Cookies = require('js-cookie');


function nodeListToArray(nodeList) {
  return Array.prototype.slice.call(nodeList, 0);
}

function clickableNavbarMenu() {
  nodeListToArray(document.querySelectorAll('.navbar-burger')).forEach((el) => {
    el.addEventListener('click', () => {
      const target = document.getElementById(el.dataset.target);
      el.classList.toggle('is-active');
      target.classList.toggle('is-active');
    });
  });
}

function callBackend(url, options) {
  const opts = Object.assign({
    credentials: 'same-origin',
    headers: {
      'X-CSRFToken': Cookies.get('csrftoken'),
    },
  }, options);
  return window.fetch(url, opts);
}

function filterCities(cities, citySelect, countrySelect) {
  let i;
  for (i = citySelect.options.length - 1; i >= 0; i -= 1) {
    citySelect.remove(i);
  }

  const country = countrySelect.value.toLowerCase();
  cities.forEach((city) => {
    const cityCountry = city.value.split('_')[1];
    if (cityCountry.toLowerCase() === country) {
      citySelect.add(city);
    }
  });
}

function settingsForm() {
  const citySelect = document.querySelector('.js-city-select');
  const countrySelect = document.querySelector('.js-country-select');
  if (citySelect && countrySelect) {
    const cities = nodeListToArray(citySelect.children);
    filterCities(cities, citySelect, countrySelect);
    countrySelect.addEventListener('change', () => filterCities(cities, citySelect, countrySelect));
  }
}

module.exports = {
  callBackend,
  clickableNavbarMenu,
  settingsForm,
};
