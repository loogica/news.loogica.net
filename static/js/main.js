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


// Gumby is ready to go
Gumby.ready(function() {


	// placeholder polyfil
	if(Gumby.isOldie || Gumby.$dom.find('html').hasClass('ie9')) {
		$('input, textarea').placeholder();
	}
});

// Oldie document loaded
Gumby.oldie(function() {

});

// Touch devices loaded
Gumby.touch(function() {

});

// Document ready
$(function() {

});

