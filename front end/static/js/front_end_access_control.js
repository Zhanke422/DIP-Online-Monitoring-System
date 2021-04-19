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
    document.getElementById("enter").innerHTML = t;

}

function leave() {
    count_leave++;
    clearInterval(setTimer);
    var li = document.createElement("li");
    var unit = (count_leave === 1) ? " time" : " times"
    li.innerHTML = "You left " + count_leave + unit
    console.log("you leaved");
    document.getElementById('messages').append(li);



}

function resize(){
    count_resize++;
    var li = document.createElement("li");
    var unit = (count_resize === 1) ? " time" : " times"
    li.innerHTML = "You resize " + count_resize + unit
    document.getElementById('record').append(li);
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
      document.getElementById('record').append(li);
    }
}

function rightClick(){
    count_rightClick++;
    clearInterval(setTimer);
    var li = document.createElement("li");
    var unit = (count_rightClick === 1) ? " time" : " times"
    li.innerHTML = "You right clicked " + count_rightClick + unit
    document.getElementById('record').append(li);
}

function paste(){
    count_paste++;
    clearInterval(setTimer);
    var li = document.createElement("li");
    var unit = (count_paste === 1) ? " time" : " times"
    li.innerHTML = "You pasted " + count_paste + unit
    document.getElementById('record').append(li);
}

window.addEventListener("focus",enter);
window.addEventListener("blur", leave);
window.addEventListener("resize",resize);
window.addEventListener("paste",paste);
window.addEventListener("contextmenu",rightClick);
//window.addEventListener("resize",resize); for refresh
