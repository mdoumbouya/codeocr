// app/static/js/app.js

$(document).ready(function(){
  console.log('app.js loaded');
  $('#run-button').click(function(e) {
      e.preventDefault();
      var source_code = $('textarea[name="source_code"]').val();
      console.log(source_code);

      $.ajax({
          type: 'POST',
          url: run_code_url,
          data: {source_code: source_code, code_picture: code_picture},
          success: function(response){
              $('#compilation-results').html(response.compilation_results);
              console.log(response.compilation_results);
          },
          error: function(error){
            console.log('error');
              console.log(error);
          }
      });
  });
});

