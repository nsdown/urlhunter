$(function () {
    $('#delete-modal').on('show.bs.modal', (e) => {
        $('.delete-form').attr('action', $(e.relatedTarget).data('href'))
    })
})