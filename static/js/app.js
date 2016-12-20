var app = angular.module('app', []);

app.controller('lightCtrl', function($scope, $http, $httpParamSerializer) {

  $scope.status = {};

  (() => {
    var eventSrc = new EventSource(ENTRIES.stream);
    eventSrc.addEventListener('update', (event) => {
      let data = JSON.parse(event.data);
      updateData(data);
      $scope.$apply();
    });
    refresh();
  })();

  function updateData(data) {
    let status = {};
    status.switch = data.switch;
    status.mode = data.mode;
    status.brightness = data.brightness;
    switch (status.mode) {
      case 1:
        status.rgb = `#${data.rgb}`;
        break;
      case 2:
        status.temp = data.temp;
        break;
    }
    $scope.status = Object.assign($scope.status, status);
    console.log($scope.status);
  }

  function refresh() {
    $http.get(ENTRIES.status)
      .then(
        (response) => {
          let data = response.data;
          updateData(data);
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
  };

  $scope.changeMode = () => {
    let mode = $scope.status.mode;
    switch (mode) {
      case 1: // RGB
        $scope.changeRgb();
        break;
      case 2:
        $scope.changeTemp();
        break;
    }
  }

  $scope.changeTemp = () => {
    let temp = $scope.status.temp;
    if (temp < 1700 || 6500 < temp) {
      return;
    }

    if ($scope.status.mode != 2) {
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
    if ($scope.status.mode != 1) {
      return;
    }

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

});
