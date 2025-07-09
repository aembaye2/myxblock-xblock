/* Javascript for MyXBlock. */
function MyXBlock(runtime, element) {
  function updateResult(result) {
    if (result.score === 1) {
      $(".result", element).text("Correct!");
    } else {
      $(".result", element).text(
        "Incorrect. The correct answer is " + result.correct_answer
      );
    }
  }

  var handlerUrl = runtime.handlerUrl(element, "submit_answer");

  $(".submit", element).click(function (eventObject) {
    var answer = $(".answer", element).val();
    $.ajax({
      type: "POST",
      url: handlerUrl,
      data: JSON.stringify({ answer: answer }),
      contentType: "application/json",
      success: updateResult,
    });
  });

  $(function ($) {
    /* Here's where you'd do things on page load. */
  });
}
