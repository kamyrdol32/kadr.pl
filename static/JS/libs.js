function coll($type, $event){
  $event.preventDefault();

  $collapse = $("div.collapse[collapse='"+$type+"']").collapse('toggle');
}



$(document).ready(function(){
  $(".content-container").mouseover(function(){
    $("body").addClass("content-hovered");
  })

  $(".content-container").mouseleave(function(){
    $("body").removeClass("content-hovered");
  })


  $("select").select2({
    minimumResultsForSearch: -1,
  });

  $("#current_company.details").on("change", function(e){
    $val = $("#current_company").val();
    window.location = "/company/list/"+$val;
  })

  $("#current_company.workers").on("change", function(e){
    $val = $("#current_company").val();
    window.location = "/company/workers/"+$val;
  })

})
