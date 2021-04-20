//
//
//
//

var setTimer;
var count_leave = 0;
var count_resize = 0;
var count_refresh = 0;
var count_paste = 0;
var count_rightClick = 0;

function myTimer() {
    var d = new Date();
    var t = d.toLocaleTimeString();
    //The innerHTML property defines the HTML content
    // document.getElementById("enter").innerHTML = t;

}

function leave() {
    count_leave++;
    clearInterval(setTimer);
    var li = document.createElement("li");
    var unit = (count_leave === 1) ? " time" : " times";
    text = " left " + count_leave + unit;
    li.innerHTML = "System Warning: You" + text;
    socket.emit('access control', "Student" + text);
    console.log("you leaved");
    document.getElementById('messages').append(li);
    if (count_leave >= 5){
      var button = document.getElementById("finish");
      button.click();
    }


}

function resize(){
    count_resize++;
    var li = document.createElement("li");
    var unit = (count_resize === 1) ? " time" : " times";
    text = " resize " + count_resize + unit;
    li.innerHTML = "System Warning: You" + text;
    document.getElementById('messages').append(li);
    socket.emit('access control', "Student" + text);
    if (count_resize >= 5){
      var button = document.getElementById("finish");
      button.click();
    }

}

function enter() {
  //setInterval() method will execute the "myTimer" function once every 1 second
  setTimer = setInterval(function(){ myTimer() }, 1000);
}

function refresh(){
    if (performance.navigation.type == performance.navigation.TYPE_RELOAD) {
      count_refresh++;
      clearInterval(setTimer);
      var li = document.createElement("li");
      var unit = (count_refresh === 1) ? " time" : " times"
      li.innerHTML = "You refreshed " + count_leave + unit
      document.getElementById('messages').append(li);
    }
}

function rightClick(){
    count_rightClick++;
    clearInterval(setTimer);
    var li = document.createElement("li");
    var unit = (count_rightClick === 1) ? " time" : " times"
    li.innerHTML = "You right clicked " + count_rightClick + unit
    document.getElementById('messages').append(li);
    if (count_rightClick >= 5){
      var button = document.getElementById("finish");
      button.click();
}

function paste(){
    count_paste++;
    clearInterval(setTimer);
    var li = document.createElement("li");
    var unit = (count_paste === 1) ? " time" : " times"
    li.innerHTML = "You pasted " + count_paste + unit
    document.getElementById('messages').append(li);
    if (count_paste >= 5){
      var button = document.getElementById("finish");
      button.click();
}

window.addEventListener("focus",enter);
window.addEventListener("blur", leave);
window.addEventListener("resize",resize);
window.addEventListener("paste",paste);
window.addEventListener("contextmenu",rightClick);
//window.addEventListener("resize",resize); for refresh
