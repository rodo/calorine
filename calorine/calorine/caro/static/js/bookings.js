
function hypaDelConfirm(uuid) {
    $('#myModal'+uuid).modal({ keyboard: false })
}

$('#deleteConfirmed').alert();
//$('#deleteConfirmed').transition(opacity .30s linear);
$('#deleteConfirmed').delay(2000).fadeOut(1500, function () { $(this).remove(); });
