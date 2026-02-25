'use strict';
{

  function initSidebarQuickFilter() {
    const options = [];
    const navSidebar = document.querySelector('.nav-sidebar');
    if (!navSidebar) {
      return;
    }
    navSidebar.querySelectorAll('.nav-sidebar .nav-item a').forEach((container) => {
      options.push({title: container.innerText.trim(), node: container});
    });

    const allNavHeaders = navSidebar.querySelectorAll('.nav-sidebar .nav-header');

    function checkValue(event) {
      let filterValue = event.target.value;
      if (filterValue) {
        filterValue = filterValue.toLowerCase();
      }
      if (event.key === 'Escape') {
        filterValue = '';
        event.target.value = ''; // clear input
      }
      let matches = false;
      for (const o of options) {
        let displayValue = '';
        if (filterValue) {
          if (o.title.toLowerCase().indexOf(filterValue) === -1) {
            displayValue = 'none';
          } else {
            matches = true;
          }
        }
        // show/hide parent <TR>
        o.node.parentNode.style.display = displayValue;
      }
      if (!filterValue || matches) {
        event.target.classList.remove('no-results');
      } else {
        event.target.classList.add('no-results');
      }

      if (!filterValue) {
        allNavHeaders.forEach(el => el.style.display = '');
      } else {
        allNavHeaders.forEach(el => el.style.display = 'none');
      }

      sessionStorage.setItem('django.admin.navSidebarFilterValue', filterValue);
    }

    const nav = document.getElementById('nav-filter');
    nav.addEventListener('change', checkValue, false);
    nav.addEventListener('input', checkValue, false);
    nav.addEventListener('keyup', checkValue, false);

    const storedValue = sessionStorage.getItem('django.admin.navSidebarFilterValue');
    if (storedValue) {
      nav.value = storedValue;
      checkValue({target: nav, key: ''});
    }
  }

  window.initSidebarQuickFilter = initSidebarQuickFilter;
  initSidebarQuickFilter();

  window.addEventListener('load', function () {
    document.getElementById('nav-filter').focus();
  });
}
