async function add_messages(message, scroll) {
  if (typeof message.name !== "undefined") {
    var date = dateNow();

    if (typeof message.time === "undefined") {
      var curr_date = date;
    } 
    else {
      var curr_date = message.time;
    }

    var global_name = await load_name();

    var content =
      '<div class="container">' +
      '<b style="color:#000000" class="right">' +
      message.name +
      "</b><p>" +
      message.message +
      '</p><span class="time-receiver">' +
      curr_date +
      "</span></div>";
    if (global_name == message.name) {
      content =
        '<div class="container darker">' +
        '<b style="color:#000" class="left">' +
        message.name +
        "</b><p>" +
        message.message +
        '</p><span class="time-sender">' +
        curr_date +
        "</span></div>";
    }
    var messageText = document.getElementById("messages");
    messageText.innerHTML += content;
  }

  if (scroll) {
    scrollSmoothToBottom("messages");
  }
}

async function load_name() {
  return await fetch("/get_name")
    .then(async function (response) {
      return await response.json();
    })
    .then(function (text) {
      return text["name"];
    });
}

async function load_messages() {
  return await fetch("/get_messages")
    .then(async function (response) {
      return await response.json();
    })
    .then(function (text) {
      console.log(text);
      return text;
    });
}

$(function () {
  $(".msgs").css({ height: $(window).height() * 0.7 + "px" });

  $(window).bind("resize", function () {
    $(".msgs").css({ height: $(window).height() * 0.7 + "px" });
  });
});

function scrollSmoothToBottom(id) {
  var div = document.getElementById(id);
  $("#" + id).animate(
    {
      scrollTop: div.scrollHeight - div.clientHeight,
    },
    500
  );
}

function dateNow() {
  var date = new Date();
  var aaaa = date.getFullYear();
  var gg = date.getDate();
  var mm = date.getMonth() + 1;

  if (gg < 10) gg = "0" + gg;

  if (mm < 10) mm = "0" + mm;

  var cur_day = aaaa + "-" + mm + "-" + gg;

  var hours = date.getHours();
  var minutes = date.getMinutes();
  var seconds = date.getSeconds();

  if (hours < 10) hours = "0" + hours;

  if (minutes < 10) minutes = "0" + minutes;

  if (seconds < 10) seconds = "0" + seconds;

  return cur_day + " " + hours + ":" + minutes;
}

let test1 = 0;
var socket = io.connect("http://" + document.domain + ":" + location.port);
socket.on("connect", async function () {
  var form = $("form#msgForm").on("submit", async function (e) {
    e.preventDefault();

    // get input from message box
    
    let message_1 = document.getElementById("msg");
    let message_2 = message_1.value;
    test1++;
    let user_name = await load_name();


    // send message to other users
    if (test1 == 1){
      socket.emit("event", {
        message: user_name + " is now active in the Chat Room. Say Hello!",
        name: user_name,
      });
    }
    socket.emit("event", {
      message: message_2,
      name: user_name,
    });
    message_1.value = "";
  });
});
socket.on("disconnect", async function (msg) {
  var usr_name = await load_name();
  socket.emit("event", {
    message: usr_name + " just left the server...",
    name: usr_name,
  });
});
socket.on("message response", function (msg) {
  add_messages(msg, true);
});

window.onload = async function () {
  var msgs = await load_messages();
  for (i = 0; i < msgs.length; i++) {
    scroll = false;
    if (i == msgs.length - 1) {
      scroll = true;
    }
    add_messages(msgs[i], scroll);
  }

  let name = await load_name();
  if (name != "") {
    $("#login").hide();
  } else {
    $("#logout").hide();
  }
};