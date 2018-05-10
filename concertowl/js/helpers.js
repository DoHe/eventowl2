const Cookies = require('js-cookie');
const Raven = require('raven-js');


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

function registerSentry() {
  Raven.config(process.env.SENTRY_PUBLIC_DSN).install();
}

module.exports = {
  callBackend,
  clickableNavbarMenu,
  registerSentry,
};
