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

function initDropDownListswithOther(){
	//Select other option Simple Tab
	//Initializations
	if($("#pillSimple #id_istheinvestmentinabuilding_12").val().toLowerCase() == 'other') $("#pillSimple .investment").removeClass('hidden'); else $("#pillSimple .investment").addClass('hidden');
	if($("#pillSimple #id_industrysector_13").val().toLowerCase() == 'other') $("#pillSimple .industrysector").removeClass('hidden'); else $("#pillSimple .industrysector").addClass('hidden');
	if($("#pillAdvanced #id_istheinvestmentinabuilding_12").val().toLowerCase() == 'other') $("#pillAdvanced .investment").removeClass('hidden'); else $("#pillAdvanced .investment").addClass('hidden');
	if($("#pillAdvanced #id_industrysector_13").val().toLowerCase() == 'other') $("#pillAdvanced .industrysector").removeClass('hidden'); else $("#pillAdvanced .industrysector").addClass('hidden');
	
	if($("#pillAdvanced #id_sourceofconsumptionbefore_35").val().toLowerCase() == 'other') $("#pillAdvanced .sourcebefore").removeClass('hidden'); else $("#pillAdvanced .sourcebefore").addClass('hidden');
	if($("#pillAdvanced #id_sourceofconsumptionafter_41").val().toLowerCase() == 'other') $("#pillAdvanced .sourceafter").removeClass('hidden'); else $("#pillAdvanced .sourceafter").addClass('hidden');
	if($("#pillAdvanced #id_whatisthebasisoftheforecast_37").val().toLowerCase() == 'other') $("#pillAdvanced .basisforecast").removeClass('hidden'); else $("#pillAdvanced .basisforecast").addClass('hidden');
	//When changing dropdownlist
	$("#pillSimple #id_istheinvestmentinabuilding_12").on('change', function() {
		if($("#pillSimple #id_istheinvestmentinabuilding_12").val().toLowerCase() == 'other') {$("#pillSimple #id_istheinvestmentinabuildingother_12").val('');$("#pillSimple .investment").removeClass('hidden');} else $("#pillSimple .investment").addClass('hidden');
	});
		$("#pillSimple #id_industrysector_13").on('change', function() {
		if($("#pillSimple #id_industrysector_13").val().toLowerCase() == 'other') {$("#pillSimple #id_industrysectorother_13").val('');$("#pillSimple .industrysector").removeClass('hidden');} else $("#pillSimple .industrysector").addClass('hidden');
	});
	$("#pillAdvanced #id_istheinvestmentinabuilding_12").on('change', function() {
		if($("#pillAdvanced #id_istheinvestmentinabuilding_12").val().toLowerCase() == 'other') {$("#pillAdvanced #id_istheinvestmentinabuildingother_12").val('');$("#pillAdvanced .investment").removeClass('hidden');} else $("#pillAdvanced .investment").addClass('hidden');
	});
		$("#pillAdvanced #id_industrysector_13").on('change', function() {
		if($("#pillAdvanced #id_industrysector_13").val().toLowerCase() == 'other') {$("#pillAdvanced #id_industrysectorother_13").val('');$("#pillAdvanced .industrysector").removeClass('hidden');} else $("#pillAdvanced .industrysector").addClass('hidden');
	});
	$("#pillAdvanced #id_sourceofconsumptionbefore_35").on('change', function() {
		if($("#pillAdvanced #id_sourceofconsumptionbefore_35").val().toLowerCase() == 'other') {$("#pillAdvanced #id_sourceofconsumptionbeforeother_35").val('');$("#pillAdvanced .sourcebefore").removeClass('hidden');} else $("#pillAdvanced .sourcebefore").addClass('hidden');
	});
	$("#pillAdvanced  #id_sourceofconsumptionafter_41").on('change', function() {
		if($("#pillAdvanced #id_sourceofconsumptionafter_41").val().toLowerCase() == 'other') {$("#pillAdvanced #id_sourceofconsumptionafterother_41").val('');$("#pillAdvanced .sourceafter").removeClass('hidden');} else $("#pillAdvanced .sourceafter").addClass('hidden');
	});
	$("#pillAdvanced  #id_whatisthebasisoftheforecast_37").on('change', function() {
		if($("#pillAdvanced #id_whatisthebasisoftheforecast_37").val().toLowerCase() == 'other') {$("#pillAdvanced #id_whatisthebasisoftheforecastother_37").val('');$("#pillAdvanced .basisforecast").removeClass('hidden');} else $("#pillAdvanced .basisforecast").addClass('hidden');
	});
};
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
	
    //Initialize Dropdownlists with other
	initDropDownListswithOther();
	//Select measure tree pop up form
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
