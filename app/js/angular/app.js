
angular.module("restApp", 
  [])

.controller("RestController", function ($scope, $rootScope, $http) {
  
  $scope.carList = [];
  $scope.car = {}
  $scope.msg = "";

  $scope.config = {
    "login": "sw",
    "senha": "rest"
  }

  $scope.clear = function () {
    $scope.car = {
      "id": "",
      "nome": "",
      "tipo": "",
      "custo": "",
    }
  }

  $scope.salvar = function ( carro ) {
    var metodo = (carro.id) ? 'PUT' : 'POST';
    var url = (carro.id) ? 'update' : 'persist';
    $http({
      method: metodo,
      url: 'http://127.0.0.1:5000/' + url,
      headers: {
        "Authorization": "Basic " + window.btoa($scope.config.login + ":" + $scope.config.senha),
        "Content-Type": "application/x-www-form-urlencoded"
      },
      data: $.param(carro)
    })
    .then(function (res) {
        console.log(res)
        $scope.clear();
        $scope.list();
      })
    .catch(function (err) {
      console.log(err)
    })    

  }

  $scope.list = function () { 
    $http.get('http://127.0.0.1:5000/all', {
      headers: {
        "Authorization": "Basic " + window.btoa($scope.config.login + ":" + $scope.config.senha)
      },
    })
      .then(function (res) {
        console.log(res)
        $scope.carList = res.data;
      })
      .catch(function (err) {
        console.log(err)
      })
  }

  $scope.get = function ( id ) {
    $http.get('http://127.0.0.1:5000/get/' + id, {
      headers: {
        "Authorization": "Basic " + window.btoa($scope.config.login + ":" + $scope.config.senha)
      },
    })
      .then(function (res) {
        console.log(res);
        $scope.car = res.data;
      })
      .catch(function (err) {
        console.log(err)
      })
  }

  $scope.list();

  $scope.delete = function(car){
    console.log("Carro",car);
    $http.delete('http://127.0.0.1:5000/delete/' + car.id, {
      headers: {
        "Authorization": "Basic " + window.btoa($scope.config.login + ":" + $scope.config.senha)
      },
    })
    .then(function (res) {
      console.log(res)
      $scope.list()

    })
    .catch(function (err) {
      console.log(err)
    })

  }  

  $scope.change = function(car){
    $scope.get(car.id);
  }  
})