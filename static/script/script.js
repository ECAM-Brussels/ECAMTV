function heure()
{
var heure=new Date();
var h=heure.getHours();
var m=heure.getMinutes();
if (h<10) {h = "0" + h}
if (m<10) {m = "0" + m}
document.getElementById('heure').innerHTML = h+":"+m;
}

function date()
{
var monthNames = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin","Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"];
var date=new Date();
document.getElementById('date').innerHTML = date.getDate()+" "+monthNames[date.getMonth()]+" "+(date.getYear()+1900);
}


function metro()
{
$('#metro1').load('/metro/1/8141').fadeIn("slow");
$('#metro2').load('/metro/1/8142').fadeIn("slow");
$('#metro3').load('/metro/79/2042').fadeIn("slow");
}


window.onload=function()
    {
  metro();
  heure();
  date();
  setInterval(heure,1000);
  setInterval(date,60000);
  setInterval(metro,30000);
    }
