document.addEventListener("DOMContentLoaded", function () {
    const stockTable = $('#stockTable').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
        },
        pageLength: 25,
        order: [[0, 'desc']],
        createdRow: function(row, data, dataIndex) {
            const cantidad = parseInt($(row).find('td:eq(7)').text());
            if (cantidad === 0) {
                $(row).addClass('bg-danger');
            } else if (cantidad < 6) {
                $(row).addClass('bg-warning');
            }
        },
        initComplete: function() {
            this.api().columns(2).every(function() {
                const column = this;
                const select = $('<select class="form-control"><option value="">Todos los Tipos</option></select>')
                    .appendTo($('#stockTable_filter').addClass('d-flex gap-2'))
                    .on('change', function() {
                        const val = $.fn.dataTable.util.escapeRegex($(this).val());
                        column.search(val ? '^'+val+'$' : '', true, false).draw();
                    });

                column.data().unique().sort().each(function(d, j) {
                    select.append('<option value="'+d+'">'+d+'</option>');
                });
            });
        }
    });

    function refreshTable() {
        stockTable.ajax.reload(null, false);
    }
});