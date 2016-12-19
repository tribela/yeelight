var app = angular.module('app', []);

app.controller('lightCtrl', function($scope, $http, $httpParamSerializer) {

  let refresh = () => {
    $http.get(ENTRIES.status)
      .then(
        (response) => {
          let data = response.data;
          console.log(data);
          $scope.status = data;
          $scope.status.rgb = `#${$scope.status.rgb}`;
          console.log(data);
        }, (response) => {
          console.debug(response.data);
        });
  }

  $scope.changeSwitch = () => {
    let power = $scope.status.switch == 1 ? 'on' : 'off';

    $http.post(ENTRIES.switch, {
      switch: power
    }).then(
      (response) => {
        console.log(response.data);
      }
    );
  }

  $scope.changeTemp = () => {
    let temp = $scope.status.temp;
    if (temp < 1700 || 6500 < temp) {
      return;
    }

    $http.post(ENTRIES.light, {
      temp: temp
    }).then(
      (response) => {
        console.log(response.data);
      }
    );
  };

  $scope.changeRgb = () => {
    let rgb = $scope.status.rgb.replace('#', '');
    $http.post(ENTRIES.light, {
      rgb: rgb
    }).then(
      (response) => {
        console.log(response.data);
      }
    );
  };

  $scope.changeBrightness = () => {
    let brightness = $scope.status.brightness;

    $http.post(ENTRIES.light, {
      brightness: brightness
    }).then(
      (response) => {
        console.log(response.data);
      }
    );
  };

  refresh();
  let handle = setInterval(refresh, 5000);
});
