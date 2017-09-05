app.service('getAlarmdepesche',function() {
  //var hostname = window.location.hostname;
  this.update = function($scope,$http) {
    //$http({
    //method: 'JSONP',
    //url: 'http://127.0.0.1:5000/api/v1.0/Alarmdepesche'
    //})
    $http.get('http://'+window.location.hostname+':5000/api/v1.0/Alarmdepesche')
       .success(function(response) {
         $scope.dicAlarmdepesche = response;
         console.log('OK');
         $scope.refreshing = true;
       })
       .error(function(response) {
         console.log('Error getting station data');
         $scope.refreshing = false;
       });
  }
});

