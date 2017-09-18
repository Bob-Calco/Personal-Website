function initMap() {
        var uluru = {lat: 51.9952667, lng: 5.8917199};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 13,
          center: uluru
        });
        var marker = new google.maps.Marker({
          position: uluru,
          map: map
        });
}
