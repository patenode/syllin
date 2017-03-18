
$(".editButton").on("click", function(event){
	if (typeof this.edit == 'undefined'){
		this.edit = true;
	}
	if (this.edit){
		$(this).html("Save");
		$(".editText").replaceWith(function () { 
			return '<input class="editTextField" type="textarea" name="' + $(this).attr("id") + '" value="' + $(this).text() + '">' 
		});
		$(".editHidden").show();
		this.edit = false;
	} else {
		$.ajax({ type: "POST",
		    url: "/update-profile",
		    cache:false,
		    data:$("input").serialize(), 
		    success: function(output){ 

		       alert("Successful Upload");

		    }

		});

		$(".editTextField").replaceWith(function () { 
			return '<span type="textarea" id="' + $(this).attr("name") +'" class="editText">' + $(this).val() + '</span>' 
		});
		this.edit = true;
		$(".editHidden").hide();
		$(this).html("Edit");

	}

});
