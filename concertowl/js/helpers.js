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

function setNotifications() {
  const counter = document.querySelector('.js-notification-count');
  const dropdown = document.querySelector('.js-notification-dropdown');
  if (!(counter && dropdown)) {
    return;
  }
  callBackend('/notifications/')
    .then(data => data.json())
    .then((json) => {
      counter.textContent = json.notifications.length;
      dropdown.innerHTML = json.notifications.map(n => `<div class="dropdown-item">${n.title}</div>`).join('\n');
    });
}

function prepareNavbar() {
  clickableNavbarMenu();
  setNotifications();
  window.setInterval(setNotifications, 5000);
}

module.exports = {
  callBackend,
  prepareNavbar,
};
