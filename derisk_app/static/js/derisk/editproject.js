function initializeTreeSimple(){
    $('#jstree_measures_div').jstree('uncheck_all')
    $('#jstree_measures_div').jstree('close_all')
	var tree_codes = [];
    $("#pillSimple #id_measures_18 > option:selected").each(function(i, item) {
	    tree_codes[i] = $(item).data('tree-code');
		$('#jstree_measures_div').jstree('check_node', tree_codes[i]);
		$('#jstree_measures_div').jstree()._open_to(tree_codes[i]);
	});
}
function initializeTreeAdvanced(){
    $('#jstree_measures_div').jstree('uncheck_all')
    $('#jstree_measures_div').jstree('close_all')
	var tree_codes = [];
    $("#pillAdvanced #id_measures_18 > option:selected").each(function(i, item) {
	    tree_codes[i] = $(item).data('tree-code');
		$('#jstree_measures_div').jstree('check_node', tree_codes[i]);
		$('#jstree_measures_div').jstree()._open_to(tree_codes[i]);
	});
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
    initializeTreeSimple();
	
	$("#pillSimple #id_measures_18").on('change', function() {
		initializeTreeSimple();
	});
	$("#pillAdvanced #id_measures_18").on('change', function() {
		initializeTreeAdvanced();
	});
    $('#flexModal').on('hidden.bs.modal', function () {
		checked_ids =[];
		for (let treeSelectedMeasure of $("#jstree_measures_div").jstree('get_checked',null,true)){
		   checked_ids.push($("#pillSimple #id_measures_18 > [data-tree-code='" + treeSelectedMeasure + "']").val());
		   checked_ids.push($("#pillAdvanced #id_measures_18 > [data-tree-code='" + treeSelectedMeasure + "']").val());
		};
		$("#pillSimple #id_measures_18").val(checked_ids).trigger("change");
		$("#pillAdvanced #id_measures_18").val(checked_ids).trigger("change");
	});

});