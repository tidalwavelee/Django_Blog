$(function () {
  function getCookie(name) {
    // Function to get any cookie available in the session.
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  function toogleVote(voteIcon, vote, data) {
    var isOwner = data.is_owner;
    if (isOwner === false) {
      if (vote === "U") {
        voteIcon.addClass('voted');
        voteIcon.siblings(`#eventDownVote`).removeClass('voted');
      } else {
        voteIcon.addClass('voted');
        voteIcon.siblings(`#eventUpVote`).removeClass('voted');
      }
      voteIcon.siblings(`#$eventVotes`).text(data.votes);
    }
  }

  var csrftoken = getCookie('csrftoken');
  var page_title = $(document).attr("title");
  // This sets up every ajax call with proper headers.
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  $("#publish").click(function () {
    // function to operate the Publish button in the event form, marking
    // the event status as published.
    $("input[name='status']").val("O");
    $("#event-form").submit();
  });

  $("#draft").click(function () {
    // Function to operate the Draft button in the event form, marking
    // the event status as draft.
    $("input[name='status']").val("D");
    $("#event-form").submit();
  });

  $(".event-vote").click(function () {
    // Vote on a event.
    var voteIcon = $(this);
    var event = $(this).closest(".event").attr("event-id");
    if ($(this).hasClass("up-vote")) {
      vote = "U";
    } else {
      $('#eventDownVote').addClass('voted');
      $('#eventUpVote').removeClass('voted');
    }
    $.ajax({
      url: '/event/event/vote/',
      data: {
        'event': event,
        'value': vote
      },
      type: 'post',
      cache: false,
      success: function (data) {
        toogleVote(voteIcon, vote, data);
      }
    });
  });

});

