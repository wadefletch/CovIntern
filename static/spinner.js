$(window).on('load', function(){
  setTimeout(removeLoader, 200); //wait for page load PLUS two seconds.
});
function removeLoader(){
    $( "#load" ).fadeOut(250, function() {
      // fadeOut complete. Remove the loading div
      $( "#load" ).remove(); //makes page more lightweight
  });  
}