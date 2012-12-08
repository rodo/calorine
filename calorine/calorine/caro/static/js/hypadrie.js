
function initboot() {
    $(".collapse").collapse();
    $('.dropdown-toggle').dropdown();
}
    


function activate_or_not() {
    
    var selecta = document.getElementById("id_nb_place_a");	      
    var ta = parseInt(selecta.options[selecta.selectedIndex].value);
    
    var selectb = document.getElementById("id_nb_place_b");	      
    if ( selectb != null ) {
	tb  = parseInt(selectb.options[selectb.selectedIndex].value);
    } else { tb = 0; }
    
    var selectc = document.getElementById("id_nb_place_c");	      
    if ( selectc != null ) {
	tc  = parseInt(selectc.options[selectc.selectedIndex].value);
    } else { tc = 0; }
    
    var selectd = document.getElementById("id_nb_place_d");
    if ( selectd != null ) {
	td = parseInt(selectd.options[selectd.selectedIndex].value);
    } else { td = 0; }
    
    var selecte = document.getElementById("id_nb_place_e");
    if ( selecte != null && selecte.type != "hidden" ) {
	te = parseInt(selecte.options[selecte.selectedIndex].value);
    } else { te = 0; }
    
    var lenname = document.getElementById("id_name").value.length + document.getElementById("id_firstname").value.length;
    
    if (document.getElementById('tarifa') != null) {
	pricea = document.getElementById('tarifa').innerHTML.replace(",",".");
    } else { pricea = "0"; }
    if (document.getElementById('tarifb') != null) {
	priceb = document.getElementById('tarifb').innerHTML.replace(",",".");
    } else { priceb = "0"; }
    if (document.getElementById('tarifc') != null) {
	pricec = document.getElementById('tarifc').innerHTML.replace(",",".");
    } else { pricec = "0"; }
    if (document.getElementById('tarifd') != null) {
	priced = document.getElementById('tarifd').innerHTML.replace(",",".");
    } else { priced = "0"; }

    if (document.getElementById('tarife') != null) {
	pricee = document.getElementById('tarife').innerHTML.replace(",",".");
    } else { pricee = "0"; }

    
    var total = ta * parseFloat(pricea) + tb * parseFloat(priceb) + tc * parseFloat(pricec) + td * parseFloat(priced) + te * parseFloat(pricee);
    
    if (( (ta + tb + tc + td + te ) * lenname) > 0 )
    {
	document.getElementById('book_btn').className='btn btn-success';
   	document.getElementById('book_btn').disabled = false;
	$('#spantotal').text('Total : ' + total.toFixed(2) + ' euros');
	$('#spantotal').show();
    }
    else 
    {
	document.getElementById('book_btn').className='btn disabled';
   	document.getElementById('book_btn').disabled = true;
	$('#spantotal').hide();
    }
}	      
