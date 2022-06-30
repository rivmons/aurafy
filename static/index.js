function reload() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function() {

        if (this.readyState != 4){
            document.getElementById("card-invalid").style.display = 'none';
            document.getElementById("card-main").style.display = 'none';
            document.getElementById("card-loader").style.display = 'grid';
        }

        else if (this.readyState == 4){

            data = JSON.parse(this.responseText);

            if (data.content == "none"){
                document.getElementById("error-msg").innerHTML = "No song currently playing :(";
                document.getElementById("card-loader").style.display = 'none';
                document.getElementById("card-main").style.display = 'none';
                document.getElementById("card-invalid").style.display = 'grid';
            }

            else if (data.content == "ad"){
                document.getElementById("error-msg").innerHTML = "Ad currently playing (broke boy) :(";
                document.getElementById("card-loader").style.display = 'none';
                document.getElementById("card-main").style.display = 'none';
                document.getElementById("card-invalid").style.display = 'grid';
            }

            else {

                document.getElementById("songname").innerHTML = data.song;
                document.getElementById("artistname").innerHTML = data.artist + '&#8212';
                document.getElementById("albumname").innerHTML = data.album;
                document.getElementById("genimg").src = data.genimg;
                document.getElementById("songimg").src = data.songimg;


                document.getElementById("card-main").style.display = 'grid';
                document.getElementById("card-loader").style.display = 'none';
            }
        }
    }

    request.open("GET", "/analyze", true);
    request.send();
}

function refresh() {
    const request = new XMLHttpRequest();
    request.onload = function() {
        console.log("refreshed successfully")
    }
    request.open("GET", "/refresh", true);
    request.send();
}