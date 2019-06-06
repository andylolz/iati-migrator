$(window).on('load', function() {
  var clipboard = new Clipboard('#copy-button');
  clipboard.on('success', function() {
    $('#copy-button').tooltip('show');
    setTimeout(function () {
      $('#copy-button').tooltip('destroy');
    }, 500);
  });
});
