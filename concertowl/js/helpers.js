const Cookies = require('js-cookie');

module.exports.nodeListToArray = nodeList => Array.prototype.slice.call(nodeList, 0);

module.exports.callBackend = (url, options) => {
  const opts = Object.assign({
    credentials: 'same-origin',
    headers: {
      'X-CSRFToken': Cookies.get('csrftoken'),
    },
  }, options);
  return window.fetch(url, opts);
};
