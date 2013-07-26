function NewsController($scope, $http) {
    // this should be done dy DI
    moment.lang('pt-br');
    $scope.moment = moment;

    $scope.news = [];
    $scope.channel = channel;

    $scope.update = function() {
        $http({
            url: '/api/news/' + $scope.channel,
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
            url: '/api/vote/' + $scope.channel + '/' + item_id,
            method: 'GET'
        }).success(function(data, status, header, config) {
            $scope.news = data.items;
        }).error(function(data, status, header, config) {
            alert('API ERROR');
        });
    };

    $scope.remove = function(item_id) {
        $http({
            url: '/api/remove/' + $scope.channel + '/' + item_id,
            method: 'GET'
        }).success(function(data, status, header, config) {
            $scope.news = data.items;
        }).error(function(data, status, header, config) {
            alert('API ERROR');
        });
    };

    $scope.open = function(channel) {
        $scope.channel = channel;
        $scope.update();
    };

    $scope.update();
}
