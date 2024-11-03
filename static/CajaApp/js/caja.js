document.addEventListener("DOMContentLoaded", function () {
    const itemsPerPage = 25;
    const cajasTableBody = document.getElementById("cajas-table-body");
    const pagination = document.getElementById("pagination");
    const cajas = Array.from(cajasTableBody.querySelectorAll("tr[data-id]"));
    let currentPage = 1;

    function renderTable(page) {
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        cajas.forEach((caja, index) => {
            caja.style.display = (index >= startIndex && index < endIndex) ? "" : "none";
        });
        const totalCajas = cajas.length;
        const currentCajas = Math.min(totalCajas - startIndex, itemsPerPage);
        document.getElementById("caja-info").textContent = `Mostrando ${currentCajas} de ${totalCajas} Cajas.`; // Cambiado aquí
        renderPagination(totalCajas);
    }

    function buscarCajas() {
        const searchInput = document.getElementById("search-input").value.toLowerCase();
        const filteredCajas = cajas.filter(caja => {
            const cajaId = caja.querySelector("td").textContent.toLowerCase();
            const empleadoNombre = caja.querySelectorAll("td")[1].textContent.toLowerCase();
            return cajaId === searchInput || empleadoNombre.includes(searchInput);
        });
        cajas.forEach(caja => caja.style.display = "none");
        filteredCajas.forEach(caja => caja.style.display = "");

        const totalFilteredCajas = filteredCajas.length;
        document.getElementById("caja-info").textContent = `Mostrando ${totalFilteredCajas} cajas.`; // Cambiado aquí
        renderPagination(totalFilteredCajas);
    }

    document.getElementById("search-btn").onclick = buscarCajas;

    document.getElementById("search-input").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            buscarCajas();
        }
    });

    window.restablecerBusqueda = function () {
        document.getElementById("search-input").value = "";
        renderTable(currentPage);
    };

    function renderPagination(totalCajas) {
        const totalPages = Math.ceil(totalCajas / itemsPerPage);
        const maxVisiblePages = 10;
        const pageNumbersContainer = document.getElementById("page-numbers");
        pageNumbersContainer.innerHTML = "";

        let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
        let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

        if (endPage - startPage < maxVisiblePages - 1) {
            startPage = Math.max(1, endPage - maxVisiblePages + 1);
        }

        for (let i = startPage; i <= endPage; i++) {
            const pageItem = document.createElement("li");
            pageItem.classList.add("page-item");
            const pageLink = document.createElement("a");
            pageLink.classList.add("page-link");
            pageLink.href = "#";
            pageLink.textContent = i;
            pageLink.onclick = function (event) {
                event.preventDefault();
                currentPage = i;
                renderTable(currentPage);
            };
            pageItem.appendChild(pageLink);
            pageNumbersContainer.appendChild(pageItem);
        }

        document.getElementById("prev-page").parentElement.classList.toggle("disabled", currentPage === 1);
        document.getElementById("next-page").parentElement.classList.toggle("disabled", currentPage === totalPages);

        document.getElementById("prev-page").onclick = function (event) {
            event.preventDefault();
            if (currentPage > 1) {
                currentPage--;
                renderTable(currentPage);
            }
        };

        document.getElementById("next-page").onclick = function (event) {
            event.preventDefault();
            if (currentPage < totalPages) {
                currentPage++;
                renderTable(currentPage);
            }
        };
    }
    renderTable(currentPage);
});
