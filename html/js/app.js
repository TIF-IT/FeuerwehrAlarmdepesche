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

    $scope.start();
});
