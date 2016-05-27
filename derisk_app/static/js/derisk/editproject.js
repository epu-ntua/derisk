function initializeTreeSimple(){
    $('#jstree_measures_div').jstree('uncheck_all')
    $('#jstree_measures_div').jstree('close_all')
    //Syncronize #simple with advanced
	$("#pillAdvanced #id_measures_18").val("").trigger("change");
	var tree_codes = [];
	var checked_ids =[];
    $("#pillSimple #id_measures_18 > option:selected").each(function(i, item) {
	    tree_codes[i] = $(item).data('tree-code');
		$('#jstree_measures_div').jstree('check_node', tree_codes[i]);
		$('#jstree_measures_div').jstree()._open_to(tree_codes[i]);
		checked_ids.push($(item).val());
	});
	if (checked_ids != $("#pillAdvanced #id_measures_18")) 
	     $("#pillAdvanced #id_measures_18").val(checked_ids).trigger("change");
}
function initializeTreeAdvanced(){
    $('#jstree_measures_div').jstree('uncheck_all')
    $('#jstree_measures_div').jstree('close_all')
    //Syncronize #simple with advanced
	$("#pillSimple #id_measures_18").val("").trigger("change");
	var tree_codes = [];
	var checked_ids =[];
    $("#pillAdvanced #id_measures_18 > option:selected").each(function(i, item) {
	    tree_codes[i] = $(item).data('tree-code');
		$('#jstree_measures_div').jstree('check_node', tree_codes[i]);
		$('#jstree_measures_div').jstree()._open_to(tree_codes[i]);
		checked_ids.push($(item).val());
	});
		if (checked_ids != $("#pillSimple #id_measures_18")) 
	     $("#pillSimple #id_measures_18").val(checked_ids).trigger("change");
}

function syncronizeSimpleWithAdvanced()
{
	    $('#pillAdvanced #id_dateinvestmentbecameoperational_29').on('change', function(e) {
           $('#pillSimple #id_dateinvestmentbecameoperational_29').val($('#pillAdvanced #id_dateinvestmentbecameoperational_29').val());
		});
	    $('#pillSimple #id_dateinvestmentbecameoperational_29').on('change', function(e) {
           $('#pillAdvanced #id_dateinvestmentbecameoperational_29').val($('#pillSimple #id_dateinvestmentbecameoperational_29').val());
		});
		$('.derisk-mirror').on('keyup', function(e) {
			var $this = $(this),
				name = $this.attr('name'),
				$otherInputs = $('.derisk-mirror[name="' + name + '"]').not(this);
				
				$otherInputs.each(function(i, otherInput) {
					$(otherInput).val($this.val())
				})
		});
		$('select.derisk-mirror').on('change', function(e) {
			var $this = $(this);
				name = $this.attr('name');
				$otherInputs = $('select.derisk-mirror[name="' + name + '"]').not(this);
				$otherInputs.each(function(i, otherInput) {
					if ($otherInputs.val() != $this.val()){
					   $otherInputs.val($this.val()).trigger("change");
					}
				})
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
	$('#pillSimple #id_dateinvestmentbecameoperational_29').datepicker({autoclose: true, viewMode: "months",minViewMode: "months",format:"mm/yyyy",todayHighlight: true});
    $('#pillAdvanced #id_dateinvestmentbecameoperational_29').datepicker({autoclose: true, viewMode: "months",minViewMode: "months",format:"mm/yyyy",todayHighlight: true});
$('#pillAdvanced #id_projectstartdate_28').datepicker({autoclose: true, viewMode: "months",minViewMode: "months",format:"mm/yyyy",todayHighlight: true});
	$('#jstree_measures_div').jstree({
		'checkbox': {
        three_state: false,
        cascade: 'up'
        },
		'plugins': ["checkbox"]
		});
    initializeTreeSimple();
	syncronizeSimpleWithAdvanced();
	$("#pillSimple #id_measures_18").on('select2:select, select2:unselect', function() {
		initializeTreeSimple();
	});
	$("#pillAdvanced #id_measures_18").on('select2:select select2:unselect', function() {
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
