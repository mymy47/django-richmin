(function () {
  'use strict';

  function start() {
    if (window.jalaliDatepicker) {
      window.jalaliDatepicker.startWatch({
        selector: 'input[data-jdp]',
        autoHide: true,
        autoShow: false,
      });

      // Explicit delegation works for tabbed fieldsets and fields added later by
      // Django formsets. The picker's built-in focus delegation is inconsistent
      // when another script changes focus during the same event.
      document.addEventListener('focusin', showPicker, true);
      document.addEventListener('click', showPicker);
    }
  }

  function showPicker(event) {
    if (event.target.matches('input[data-jdp]')) {
      window.jalaliDatepicker.show(event.target);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
