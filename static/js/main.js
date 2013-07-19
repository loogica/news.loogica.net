function NewsController($scope, $http) {
    $scope.news = [];

    // this should be done dy DI
    $scope.moment = moment;

    $scope.update = function() {
        $http({
            url: '/api/news',
            method: 'GET'
        }).success(function(data, status, header, config) {
            $scope.news = data.items;
            $scope.show_items = true;
        }).error(function(data, status, header, config) {
            alert('API ERROR');
        });
    };

    $scope.vote = function(item_id) {
        $http({
            url: '/api/vote/' + item_id,
            method: 'GET'
        }).success(function(data, status, header, config) {
            $scope.news = data.items;
        }).error(function(data, status, header, config) {
            alert('API ERROR');
        });
    };

    $scope.remove = function(item_id) {
        $http({
            url: '/api/remove/' + item_id,
            method: 'GET'
        }).success(function(data, status, header, config) {
            $scope.news = data.items;
        }).error(function(data, status, header, config) {
            alert('API ERROR');
        });
    };

    $scope.update();
}
