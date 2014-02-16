var news = angular.module('looginews', []);

news.controller('NewsController',
    function($scope, $http) {
        // this should be done dy DI
        moment.lang('pt-br');
        $scope.moment = moment;

        $scope.news = [];
        $scope.channel = channel;
        $scope.item_id = item_id;
        $scope._date_sort_flag = true;

        var _process_items = function(items) {
            _.each(items, function(item) {
                item.date_posted = moment(item.posted);
            });
            return items;
        };

        $scope.update = function() {
            if ($scope.item_id) {
                $http({
                    url: '/api/' + $scope.channel + '/' + $scope.item_id,
                    method: 'GET'
                }).success(function(data, status, header, config) {
                    $scope.news = _process_items([data.item]);
                    $scope.show_items = true;
                }).error(function(data, status, header, config) {
                    alert('API ERROR');
                });
            } else {
                $http({
                    url: '/api/news/' + $scope.channel,
                    method: 'GET'
                }).success(function(data, status, header, config) {
                    $scope.news = _process_items(data.items);
                    $scope.show_items = true;
                }).error(function(data, status, header, config) {
                    alert('API ERROR');
                });
            }
        };

        $scope.vote = function(item_id) {
            $http({
                url: '/api/vote/' + $scope.channel + '/' + item_id,
                method: 'GET'
            }).success(function(data, status, header, config) {
                $scope.news = _process_items(data.items);
            }).error(function(data, status, header, config) {
                alert('API ERROR');
            });
        };

        $scope.remove = function(item_id) {
            $http({
                url: '/api/remove/' + $scope.channel + '/' + item_id,
                method: 'GET'
            }).success(function(data, status, header, config) {
                $scope.news = _process_items(data.items);
            }).error(function(data, status, header, config) {
                alert('API ERROR');
            });
        };

        $scope.sort_date = function() {
             var items = _.sortBy($scope.news, function(element) {
                return element.date_posted;
            });
            if ($scope._date_sort_flag) {
                $scope.news = items.reverse();
            } else {
                $scope.news = items;
            }
            $scope._date_sort_flag = !$scope._date_sort_flag;
        };

        $scope.open = function(channel) {
            $scope.channel = channel;
            $scope.update();
        };

        $scope.update();
    }
);
