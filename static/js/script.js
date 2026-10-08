/* =========================================
   FULL GOSPEL CHURCH WEBSITE
   MAIN JAVASCRIPT
   ========================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =========================================
       MOBILE MENU
       ========================================= */

    const menuButton = document.getElementById("menu-toggle");
    const navMenu = document.getElementById("site-sidebar");

    if (menuButton && navMenu) {
        menuButton.addEventListener("click", function () {
            const isExpanded = menuButton.getAttribute("aria-expanded") === "true";
            navMenu.hidden = isExpanded;
            menuButton.setAttribute("aria-expanded", String(!isExpanded));
            menuButton.setAttribute("aria-label", isExpanded ? "Open menu" : "Close menu");
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
                menuButton.click();
                menuButton.focus();
            }
        });
    }


    /* =========================================
       CLOSE MOBILE MENU WHEN LINK IS CLICKED
       ========================================= */

    const navLinks = document.querySelectorAll(".nav-item");

    navLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            if (navMenu && menuButton) {
                navMenu.hidden = true;
                menuButton.setAttribute("aria-expanded", "false");
                menuButton.setAttribute("aria-label", "Open menu");
            }
        });
    });


    /* =========================================
       SEARCH
       ========================================= */

    const searchInput = document.getElementById("site-search");
    const searchableItems = document.querySelectorAll(".nav-item");
    const noResults = document.getElementById("no-results");

    if (searchInput) {
        searchInput.addEventListener("input", function () {

            const searchText = searchInput.value.toLowerCase().trim();
            let visibleCount = 0;

            searchableItems.forEach(function (item) {

                const itemText = item.textContent.toLowerCase();

                const matches = itemText.includes(searchText);
                item.style.display = matches ? "" : "none";
                if (matches) {
                    visibleCount += 1;
                }

            });

            if (noResults) {
                noResults.hidden = visibleCount > 0;
            }

            if (searchText && navMenu && menuButton) {
                navMenu.hidden = false;
                menuButton.setAttribute("aria-expanded", "true");
                menuButton.setAttribute("aria-label", "Close menu");
            }
        });
    }


    /* =========================================
       SCROLL TO TOP BUTTON
       ========================================= */

    const scrollTopButton = document.getElementById("scrollTopButton");

    if (scrollTopButton) {

        window.addEventListener("scroll", function () {

            if (window.scrollY > 300) {
                scrollTopButton.classList.add("show");
            } else {
                scrollTopButton.classList.remove("show");
            }

        });

        scrollTopButton.addEventListener("click", function () {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        });
    }


    /* =========================================
       SMOOTH SCROLLING
       ========================================= */

    const smoothLinks = document.querySelectorAll('a[href^="#"]');

    smoothLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const targetId = this.getAttribute("href");

            if (targetId !== "#") {

                const target = document.querySelector(targetId);

                if (target) {

                    event.preventDefault();

                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                }
            }

        });

    });


    /* =========================================
       FADE-IN ANIMATION
       ========================================= */

    const animatedElements = document.querySelectorAll(".fade-in");

    const observer = "IntersectionObserver" in window && new IntersectionObserver(
        function (entries) {

            entries.forEach(function (entry) {

                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                }

            });

        },
        {
            threshold: 0.15
        }
    );

    if (observer) {
        animatedElements.forEach(function (element) {
            observer.observe(element);
        });
    }


    /* =========================================
       CURRENT YEAR
       ========================================= */

    const yearElement = document.getElementById("currentYear");

    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }


    /* =========================================
       CLOSE ALERT / NOTIFICATION
       ========================================= */

    const closeButtons = document.querySelectorAll(".close-alert");

    closeButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const alertBox = button.closest(".alert");

            if (alertBox) {
                alertBox.style.display = "none";
            }

        });

    });


    /* =========================================
       CONFIRM DELETE
       ========================================= */

    const deleteButtons = document.querySelectorAll(".delete-confirm");

    deleteButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this item?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });

});
