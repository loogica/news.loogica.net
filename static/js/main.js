function NewsController($scope, $http) {
    $scope.news = [];
    $scope.update = function() {
        $http({
            url: '/api/news',
            method: 'GET'
        }).success(function(data, status, header, config) {
            $scope.news = data.items;
        }).error(function(data, status, header, config) {
            alert('API ERROR');
        });
    }
    $scope.update();

    $scope.vote = function(item_id) {
        $http({
            url: '/api/vote/' + item_id,
            method: 'GET'
        }).success(function(data, status, header, config) {
            $scope.news = data.items;
        }).error(function(data, status, header, config) {
            alert('API ERROR');
        })
    }

    $scope.moment = moment;
}
