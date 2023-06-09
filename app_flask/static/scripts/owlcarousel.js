$(document).ready(function() {
  var owl = $('.owl-carousel');
    owl.owlCarousel({
      items : 4,
      autoPlay: true,
      smartSpeed: 700,
      dots:false,
      autoplay:true,
      // autoplayHoverPause:true,
      loop:true,
      responsive: {
        600: {
          items: 4
        }
      }
    });

    $(".btnPlayOwlCarousel").click(function(){
      console.log("btnClicked");
      owl.trigger('play.owl.autoplay', [1000]);

    })
  });