function initMap() {
        var uluru = {lat: 51.9952431, lng: 5.8897835};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 13,
          center: uluru
        });
        var marker = new google.maps.Marker({
          position: uluru,
          map: map
        });
}
