///////////////////////////////////////////////////////////
// mobile navigation
const btnNavEl = document.querySelector(".btn-mobile-nav");
const headerEl = document.querySelector(".header");

btnNavEl.addEventListener("click", function () {
  headerEl.classList.toggle("nav-open");
});

///////////////////////////////////////////////////////////
// Close mobile navigation

const allLinks = document.querySelectorAll(".main-nav-link");

allLinks.forEach(function (link) {
  link.addEventListener("click", function (e) {
    if (link.classList.contains("main-nav-link"))
      headerEl.classList.toggle("nav-open");
  });
});

///////////////////////////////////////////////////////////
// Fixing flexbox gap property missing in some Safari versions
function checkFlexGap() {
  var flex = document.createElement("div");
  flex.style.display = "flex";
  flex.style.flexDirection = "column";
  flex.style.rowGap = "1px";

  flex.appendChild(document.createElement("div"));
  flex.appendChild(document.createElement("div"));

  document.body.appendChild(flex);
  var isSupported = flex.scrollHeight === 1;
  flex.parentNode.removeChild(flex);

  if (!isSupported) document.body.classList.add("no-flexbox-gap");
}
checkFlexGap();

///////////////////////////////////////////////////////////
// Toggling homework `done` attribute
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
$(document).ready(function() {
  $('.toggle-btn').click(function() {
    var endpoint = $(this).data('endpoint');
    var csrftoken = getCookie('csrftoken');
    var homeworkCard = $(this).parent().parent();
    $.ajax({
      url: window.location.origin + endpoint,
      type: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      success: function(response) {
        homeworkCard.toggleClass('card_success');
      }
    });
  });
});