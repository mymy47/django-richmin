'use strict';
{

  function setTheme(mode) {
    if (mode !== "light" && mode !== "dark" && mode !== "auto") {
      console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
      mode = "auto";
    }
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const effectiveTheme = mode === "auto" ? (prefersDark ? "dark" : "light") : mode;
    document.documentElement.dataset.theme = effectiveTheme;
    document.documentElement.dataset.themeMode = mode;
    localStorage.setItem("theme", mode);

    const navbar = document.querySelector('.navbar');
    const bodyTag = document.querySelector('body');
    const contentWrapper = document.querySelector('.content-wrapper');
    const mainFooter = document.querySelector('.main-footer');
    if (effectiveTheme === 'dark') {
      // Is in dark theme

      if (!!navbar) {
        navbar.classList.remove('navbar-white', 'navbar-light');
        navbar.classList.add('navbar-dark');
      }

      if (!!bodyTag) {
        bodyTag.classList.add('bg-dark', 'text-white');
      }

      if (!!contentWrapper) {
        contentWrapper.classList.add('bg-dark', 'text-white');
      }

      if (!!mainFooter) {
        mainFooter.classList.add('bg-dark', 'text-white');
      }
    } else {
      if (!!navbar) {
        navbar.classList.remove('navbar-dark');
        navbar.classList.add('navbar-white', 'navbar-light');
      }

      if (!!bodyTag) {
        bodyTag.classList.remove('bg-dark', 'text-white');
      }

      if (!!contentWrapper) {
        contentWrapper.classList.remove('bg-dark', 'text-white');
      }

      if (!!mainFooter) {
        mainFooter.classList.remove('bg-dark', 'text-white');
      }
    }
  }

  function initTheme() {
    // set theme defined in localStorage if there is one, or fallback to auto mode
    const currentTheme = localStorage.getItem("theme");
    currentTheme ? setTheme(currentTheme) : setTheme("auto");
  }

  initTheme();

  const colorSchemeQuery = window.matchMedia("(prefers-color-scheme: dark)");
  const syncAutoTheme = function () {
    if ((localStorage.getItem("theme") || "auto") === "auto") {
      setTheme("auto");
    }
  };
  if (colorSchemeQuery.addEventListener) {
    colorSchemeQuery.addEventListener("change", syncAutoTheme);
  } else {
    colorSchemeQuery.addListener(syncAutoTheme);
  }

  window.addEventListener('load', function (e) {

    function cycleTheme() {
      const currentTheme = localStorage.getItem("theme") || "auto";
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

      if (prefersDark) {
        // Auto (dark) -> Light -> Dark
        if (currentTheme === "auto") {
          setTheme("light");
        } else if (currentTheme === "light") {
          setTheme("dark");
        } else {
          setTheme("auto");
        }
      } else {
        // Auto (light) -> Dark -> Light
        if (currentTheme === "auto") {
          setTheme("dark");
        } else if (currentTheme === "dark") {
          setTheme("light");
        } else {
          setTheme("auto");
        }
      }
    }

    function setupTheme() {
      // Attach event handlers for toggling themes
      const buttons = document.getElementsByClassName("theme-toggle");
      Array.from(buttons).forEach((btn) => {
        btn.addEventListener("click", cycleTheme);
      });
      initTheme();
    }

    setupTheme();
  });
}
