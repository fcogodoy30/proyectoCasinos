$(document).ready(function() {
    // Initialize DataTable
    $('#menu-table').DataTable({
        "paging": true,
        "searching": true,
        "ordering": true,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.11.3/i18n/es_es.json"  // Localization for Spanish
        }
    });
});