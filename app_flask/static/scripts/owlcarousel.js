$(document).ready(function() {
  var owl = $('.owl-carousel');
    owl.owlCarousel({
      items : 4,
      autoPlay: true,
      smartSpeed: 700,
      dots:false,
      autoplay:true,
      autoplayHoverPause:true,
      loop:true,
      responsive: {
        600: {
          items: 4
        }
      }
    });

    // $(".btnStopOwlCarousel").click(function(){
    //   owl.trigger('stop.owl.autoplay');
    //    if ($(".btnStopOwlCarousel").text() === "STOP"){
    //     console.log("Is Stop");
    //     $(".btnStopOwlCarousel").text("PLAY");
    //    };
    //   //  $(".btnStopOwlCarousel").text("STOP");
    // })
  });