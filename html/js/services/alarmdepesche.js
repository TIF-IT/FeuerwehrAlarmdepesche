app.service('getAlarmdepesche',function() {
  this.update = function($scope,$http) {
    $http({
    method: 'JSONP',
    url: 'http://127.0.0.1:5000/api/v1.0/Alarmdepesche'
    })
       .success(function(data) {
         $scope.dicAlarmdepesche = data.Alarmdepesche;
         console.log('OK');
         $scope.refreshing = true;//false;
       })
       .error(function(data) {
         console.log('Error getting station data');
         $scope.refreshing = false;
       });
  }
});

