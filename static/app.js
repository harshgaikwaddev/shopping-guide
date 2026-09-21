function fillLocation() {
  if (!navigator.geolocation) {
    alert("Geolocation is not supported by this browser.");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    function (position) {
      var latInput = document.getElementById("latInput");
      var lngInput = document.getElementById("lngInput");
      if (latInput && lngInput) {
        latInput.value = position.coords.latitude.toFixed(6);
        lngInput.value = position.coords.longitude.toFixed(6);
      }
    },
    function () {
      alert("Unable to fetch location.");
    }
  );
}
