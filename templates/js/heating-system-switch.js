
function check_switch_status(){
  $.getJSON('https://la-madriguera-iot.herokuapp.com/heating-system/getStatus', function(data) {
    document.getElementById("switch").checked = data[0].status;
  });
}

window.onload = check_switch_status();
