$(document).ready(function () {
	$('[data-toggle="tooltip"]').tooltip();
	$('form input, form textarea').addClass('form-control');
	$('form select').select2({width: '100%'});
});