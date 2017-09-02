var app = angular.module('root', []);
app.controller('Alarmdepesche',function($scope,$http,getAlarmdepesche) {
    // refreshing
    console.log('Start controller');
    $scope.refreshing = true;
    $scope.refreshMessage = 'Loading';
    
    console.log('Define starter');
    $scope.start = function() {
      console.log('Start starter');

      getAlarmdepesche.update($scope,$http);

      // show our app
      $scope.show_app = true;
    }

    $scope.start();
});
