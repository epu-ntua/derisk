function initializeTree(){
}
$(document).ready(function () {
	$('[data-toggle="tooltip"]').tooltip();
	$('form input, form textarea').addClass('form-control');
	$('form select').select2({width: '100%'});
    $('#jstree_measures_div').jstree({
		'checkbox': {
        three_state: false,
        cascade: 'up'
        },
		'plugins': ["checkbox"]
		});
});