$( document ).ready(function() {
<<<<<<< HEAD
    $(".getstarted").click(function(){
      $("#b").animate({top:"-50vh",height:"100vh"},500);
      $(".main").animate({top:"-30vh"},500);
    });
    $(".upload").click(function(){
      $(".indeterminate").addClass("blue-grey lighten-5");
    });
    $(".links").click(function(){
      if($(".description").hasClass("attop")==true)
      {
        $(".description").removeClass("attop").animate({top:"100vh"},500);
      }
      else
      $(".description").animate({top:"50vh"},500).addClass("attop");
      
    });
=======
  $(".getstarted").click(function(){
    $("#b").animate({top:"-50vh",height:"100vh"},500);
    $(".main").animate({top:"-30vh"},500);
  });
  $(".upload").click(function(){
    $(".indeterminate").addClass("blue-grey lighten-5");
  });

>>>>>>> 8333dbf250ce3d41599704f8340435af7dcbb951
});
