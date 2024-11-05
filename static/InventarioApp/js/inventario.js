document.addEventListener("DOMContentLoaded", function () {
    const itemsPerPage = 25;
    const stockTableBody = document.getElementById("stock-table-body");
    const pagination = document.getElementById("pagination");
    const products = Array.from(stockTableBody.querySelectorAll("tr[data-id]"));
    let currentPage = 1;

    function renderTable(page) {
      const startIndex = (page - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      products.forEach((product, index) => {
        product.style.display = (index >= startIndex && index < endIndex) ? "" : "none";
      });
      const totalProducts = products.length;
      const currentProducts = Math.min(totalProducts - startIndex, itemsPerPage);
      document.getElementById("product-info").textContent = `Mostrando ${currentProducts} de ${totalProducts} productos.`;
      renderPagination(totalProducts);
    }

    function renderPagination(totalProducts) {
      const totalPages = Math.ceil(totalProducts / itemsPerPage);
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

    function buscarProductos() {
      const searchInput = document.getElementById("search-input").value.toLowerCase();
    
      const filteredProducts = products.filter(product => {
        const productId = product.querySelector("td").textContent.toLowerCase();
        const productDescription = product.querySelectorAll("td")[1].textContent.toLowerCase();
        return productId.includes(searchInput) || productDescription.includes(searchInput);
      });
    
      products.forEach(product => product.style.display = "none");
      filteredProducts.forEach(product => product.style.display = "");
    
      const totalFilteredProducts = filteredProducts.length;
      document.getElementById("product-info").textContent = `Mostrando ${totalFilteredProducts} productos.`;
      renderPagination(totalFilteredProducts);
    }
    

    document.getElementById("search-btn").onclick = buscarProductos;

    document.getElementById("search-input").addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        buscarProductos();
      }
    });

    window.restablecerBusqueda = function () {
      document.getElementById("search-input").value = "";
      renderTable(currentPage);
    };

    document.getElementById("filter-btn").onclick = function () {
      const selectedType = document.getElementById("filter-select").value;
      products.forEach(product => {
        const productType = product.querySelectorAll("td")[2].textContent;
        product.style.display = (selectedType === "" || productType === selectedType) ? "" : "none";
      });

      const totalFilteredProducts = products.filter(product => product.style.display !== "none").length;
      document.getElementById("product-info").textContent = `Mostrando ${totalFilteredProducts} productos.`;
      renderPagination(totalFilteredProducts);
    };

    renderTable(currentPage);
  });