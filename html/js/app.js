var app = angular.module('root', []);
app.controller('Alarmdepesche',function($scope,$http,$interval,getAlarmdepesche) {
    // refreshing
    console.log('Start controller');
    $scope.refreshing = true;
    $scope.refreshMessage = 'Loading';
    
    console.log('Define starter');
    $scope.start = function() {
      console.log('Start starter');

      $interval(function() {
        //$scope.date = new Date();
        //$scope.time = $scope.date.getTime();
	      getAlarmdepesche.update($scope,$http);
      }, 3000);


      //getAlarmdepesche.update($scope,$http);

      // show our app
      $scope.show_app = true;
    }

    $scope.initOpenStreetmap = function () {
      

      map = new OpenLayers.Map("Map");
      
      var lat = $scope.dicAlarmdepesche.Target.GeoLat;
      var long = $scope.dicAlarmdepesche.Target.GeoLong;
  
      var mapnik         = new OpenLayers.Layer.OSM();
      var fromProjection = new OpenLayers.Projection("EPSG:4326");   // Transform from WGS 1984
      var toProjection   = new OpenLayers.Projection("EPSG:900913"); // to Spherical Mercator Projection
      var position       = new OpenLayers.LonLat(long, lat).transform( fromProjection, toProjection);
      var zoom           = 15; 
  
      map.addLayer(mapnik);

      //new Point(fromLonLat([long, lat]))
      /*var rome = new Feature({
        geometry: new Point(fromLonLat([long, lat]))
      });*/
  
      var pois = new OpenLayers.Layer.Text( "My Points",
                  { location:"./openStreetMaps/poi.txt",
                    projection: map.displayProjection
                  });
      map.addLayer(pois);
  
      var layer_switcher= new OpenLayers.Control.LayerSwitcher({});
      map.addControl(layer_switcher);
  
  
      map.setCenter(position, zoom );

      /*export map https://openlayers.org/en/latest/examples/export-pdf.html
      map.once('rendercomplete', function(event) {
          var canvas = event.context.canvas;
          if (navigator.msSaveBlob) {
            navigator.msSaveBlob(canvas.msToBlob(), 'map.png');
          } else {
            canvas.toBlob(function(blob) {
              saveAs(blob, 'map.png');
            });
          }
        });
        map.renderSync();*/
    }

    $scope.start();
});
