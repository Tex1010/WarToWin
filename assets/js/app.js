document.addEventListener("DOMContentLoaded", () => {

    const navbar = `
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">

            <a class="navbar-brand fw-bold" href="index.html">
                <img src="assets/img/logo.png" height="50">
                War To Win
            </a>

            <button class="navbar-toggler"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">

                <ul class="navbar-nav ms-auto">

                    <li class="nav-item">
                        <a class="nav-link" href="members.html">
                            Membres
                        </a>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link" href="rules.html">
                            Règlement
                        </a>
                    </li>

                </ul>

            </div>

        </div>
    </nav>
    `;

    const footer = `
    <footer class="footer mt-5">

        <div class="container text-center">

            <h5>War To Win (W2W)</h5>

            <p>Force • Discipline • Victoire</p>

            <p class="small">
                © 2026 War To Win Team
            </p>

        </div>

    </footer>
    `;

    const navbarContainer = document.getElementById("navbar-container");
    const footerContainer = document.getElementById("footer-container");

    if (navbarContainer) {
        navbarContainer.innerHTML = navbar;
    }

    if (footerContainer) {
        footerContainer.innerHTML = footer;
    }

});