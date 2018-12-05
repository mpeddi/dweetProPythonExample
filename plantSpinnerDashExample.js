$.support.cors = true;

setTimeout(function(){

	$('#spinButton').click(function(e){
		e.preventDefault();
		window.sendSpin();
	});

},3000);

var spin_payload =  {
				"thing": "testie",
				"key": "AsiBr-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-XXX",
				"content": {
					"spin_toggle": 1
				}
		  };

window.sendSpin = function() {
	if (true) {
		$.ajax({
		  type: "POST",
		  url: "https://dweetpro.io/v2/dweets",
		  headers: {
				"Content-type": "application/json",
				"X-DWEET-AUTH": "eyJyb2XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
			},
		contentType: "application/json; charset=utf-8",
        dataType: "json",
		  data: JSON.stringify(spin_payload)
		 }).done(function(response) {
			 freeboard.showLoadingIndicator(true);
				 setTimeout(function(){
					 freeboard.showLoadingIndicator(false);
				 },1000);
		 });
	}
}
