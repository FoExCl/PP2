function confirmDelete() {
    if (confirm("¿Estás seguro de que deseas borrar este producto?")) {
      window.location.href = "{% url 'borrar_producto' producto.id_productos %}";
    }
  }