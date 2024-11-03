document.addEventListener('DOMContentLoaded', function() {
    const totalElement = document.getElementById('total');
    const facturaNumero = document.getElementById('numero-factura');
    const clienteInput = document.getElementById('cliente');
    const codigoInput = document.getElementById('codigo');
    const articuloInput = document.getElementById('articulo');
    const cantidadInput = document.getElementById('cantidad');
    const precioInput = document.getElementById('precio');
    

    let seleccionado = false;

    function generateFacturaNumber() {
        return Math.floor(Math.random() * 1000000).toString().padStart(6, '0');
    }

    facturaNumero.value = generateFacturaNumber();

    function eliminar(fila) {
        fila.remove();
        actualizarTotal();
        console.log("Producto eliminado");
    }

    function cambiar(fila) {
        let nuevoNombre = prompt("Ingrese el nuevo nombre del producto:", fila.cells[1].textContent);
        let nuevoPrecio = prompt("Ingrese el nuevo precio:", fila.cells[2].textContent);
        let nuevaCantidad = prompt("Ingrese la nueva cantidad:", fila.cells[0].textContent);
        
        if (nuevoNombre && nuevoPrecio && nuevaCantidad) {
            nuevoPrecio = parseFloat(nuevoPrecio);
            nuevaCantidad = parseInt(nuevaCantidad);
            
            if (!isNaN(nuevoPrecio) && !isNaN(nuevaCantidad) && nuevaCantidad > 0) {
                fila.cells[0].textContent = nuevaCantidad;
                fila.cells[1].textContent = nuevoNombre;
                fila.cells[2].textContent = (nuevoPrecio * nuevaCantidad).toFixed(2);
                actualizarTotal();
                console.log("Producto cambiado");
            } else {
                alert("Por favor, ingrese valores válidos para precio y cantidad.");
            }
        }
    }
function filtrarTabla() {
      // Obtener el valor del campo de entrada
      var input, filter, table, tr, td, i, txtValue;
      input = document.getElementById("filtroCodigo");
      filter = input.value.toUpperCase();
      table = document.getElementById("miTabla");
      tr = table.getElementsByTagName("tr");

      // Recorrer todas las filas y ocultar las que no coincidan con el filtro
      for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0]; // Obtener la celda del código
        if (td) {
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
          }
        }
      }
    }
    document.querySelector('.btn-5').addEventListener('click', function() {
        const codigo = codigoInput.value;
        const articulo = articuloInput.value;
        const cantidad = parseFloat(cantidadInput.value);
        const precio = parseFloat(precioInput.value);

        if (codigo && articulo && !isNaN(cantidad) && !isNaN(precio)) {
            const tabla = document.querySelector('.table tbody');
            const nuevaFila = document.createElement('tr');

            nuevaFila.innerHTML = `
    <th scope="row">${cantidad}</th>
    <td>${articulo}</td>
    <td>${(precio * cantidad).toFixed(2)}</td>
    <td>
    <button type="submit" class="btn-eliminar"><i class="fa-solid fa-trash"></i></button>

        <button type="submit" class="btn-cambiar"><i class="fa-solid fa-pen-to-square"></i></button>
    </td>
            `;

            tabla.appendChild(nuevaFila);

            nuevaFila.querySelector(".btn-eliminar").addEventListener('click', () => eliminar(nuevaFila));
            nuevaFila.querySelector(".btn-cambiar").addEventListener('click', () => cambiar(nuevaFila));

            actualizarTotal();
        } else {
            alert('Por favor, complete todos los campos correctamente.');
        }
    });

    function actualizarTotal() {
        const filas = document.querySelectorAll('.table tbody tr');
        let total = 0;

        filas.forEach(fila => {
            const precioVenta = parseFloat(fila.cells[2].textContent.replace(',', '.'));
            if (!isNaN(precioVenta)) {
                total += precioVenta;
            }
        });

        totalElement.textContent = total.toFixed(2);
    }
    document.querySelector('.btn-1').addEventListener('click', function() {
        // Aquí iría la lógica para actualizar precios desde el servidor
        
        console.log("Actualizar precios (funcionalidad no implementada)");
    });

    document.querySelector('.btn-2').addEventListener('click', function() {
        const filas = document.querySelectorAll('.table tbody tr');
        if (filas.length > 0) {
            filas[filas.length - 1].remove();
            actualizarTotal();
        } else {
            alert('No hay productos para eliminar.');
        }
    });

    document.querySelector('.btn-3').addEventListener('click', function() {
        if (clienteInput.value.trim() === '') {
            alert('Por favor, ingrese el nombre del cliente.');
        } else {
            alert(`Factura generada para el cliente: ${clienteInput.value}`);
            location.reload();
        }
    });

    document.querySelector('.btn-4').addEventListener('click', function() {
        if (confirm("¿Estás seguro de que quieres cerrar la ventana?")) {
          window.close();
        }
      });
    });