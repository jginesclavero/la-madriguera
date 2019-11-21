
function check_switch_status(){
  $.getJSON('url/heating-system/getStatus', function(data) {
    document.getElementById("switch").checked = data[0].status;
  });
}

window.onload = check_switch_status();
