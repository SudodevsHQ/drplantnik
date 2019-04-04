$( document ).ready(function() {
  $(".getstarted").click(function(){
    $("#b").animate({top:"-50vh",height:"100vh"},500);
    $(".main").animate({top:"-30vh"},500);
  });
  $(".upload").click(function(){
    $(".indeterminate").addClass("blue-grey lighten-5");
  });

});
