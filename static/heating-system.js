function check_status(){
  $.getJSON('https://la-madriguera-iot.herokuapp.com/heating-system/getStatus', function(data) {
    document.getElementById("switch").value = data[0].status;
    document.getElementById("temp").value = data[0].temp;
  });
  document.getElementById("switch").value = false;
  document.getElementById("temp").value = 17;
}
  
function temp_button(element){
  var url = "https://la-madriguera-iot.herokuapp.com/heating-system/setTemp?temp=" + element.value;
  $.get(url);
}

function toggleonfoff_init() {
  document.getElementById("switch").value = 0;
  document.getElementById("temp").value = 17;

  $.getJSON('https://la-madriguera-iot.herokuapp.com/heating-system/getStatus', function(data) {
    document.getElementById("switch").value = data[0].status;
    document.getElementById("temp").value = data[0].temp;
  })

  if (document.getElementById("switch").value == 1) {
    $("div.input.toggle-onoff input:hidden").parent("div").children("i.fa").removeClass("fa-toggle-on").addClass("fa-toggle-off");
    $("div.input.toggle-onoff input:hidden[value=1]").parent("div").children("i.fa").removeClass("fa-toggle-off").addClass("fa-toggle-on");
  } else {
    $("div.input.toggle-onoff input:hidden").parent("div").children("i.fa").removeClass("fa-toggle-off").addClass("fa-toggle-on");
    $("div.input.toggle-onoff input:hidden[value=0]").parent("div").children("i.fa").removeClass("fa-toggle-on").addClass("fa-toggle-off");
  }  
}

$("div.input.toggle-onoff").click(function() {
  var value = $(this).children("input:hidden").val();
  if (value == 1) {
    $(this).children("input:hidden").val(0);
    $(this).children("i.fa").removeClass("fa-toggle-on").addClass("fa-toggle-off");
    value = 0;
  } else {
      $(this).children("input:hidden").val(1);
      $(this).children("i.fa").removeClass("fa-toggle-off").addClass("fa-toggle-on");
      value = 1;
  }
  console.log($(this).children("input:hidden").val());
  var url = "http://la-madriguera-iot.herokuapp.com/heating-system/setStatus?status=" + value;
  $.get(url);
});

$(document).ready(function() { 
  toggleonfoff_init();
});
