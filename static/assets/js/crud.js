$(document).ready(function(){
    $('#id_group_salary').addClass('form-control');
    $('#id_date_joined').addClass('form-control');
    $("#id_date_joined").prop("type", "date");
    $('#edit_modal select').addClass('form-control');
    $('#edit_modal #id_date_joined').addClass('form-control');
    $("#edit_modal #id_date_joined").prop("type", "date");
    
    $('#add_employee_form').submit(function(e){
        e.preventDefault();
        var thisForm = $(this);
        var action = thisForm.attr('action')
        var formData = thisForm.serialize()

        $.ajax({
            url: action,
            method: 'post',
            data: formData,
            success: function(data){
                if(data.added){
                    $.confirm({
                        title: 'Succès!',
                        content: 'Employé ajouté avec succès',
                        type: 'green',
                        typeAnimated: true,
                        buttons: {
                            tryAgain: {
                                text: 'OK',
                                btnClass: 'btn-green',
                                action: function(){
                                }
                            },
                            close: function () {
                            }
                        }
                    });
                    $('#add_employee_form')[0].reset();
                    $('#datatable-buttons tbody').html(data.salaries)
                }
            },
            error: function(data){
                console.log(data)
            }
        })
    });



    $('.edit_button').click(function(){
        var btn = $(this);
        var url = btn.attr('data-url');

        $.ajax({
            url: url,
            method: 'get',
            success: function(data){
                $("#edit").html(data.html_form)
                console.log(data)
            }
        })
    })
});