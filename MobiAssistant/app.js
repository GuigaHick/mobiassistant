var app = angular.module('cdg', [require('angular-route'),'angularUtils.directives.dirPagination']);

app.config(function($routeProvider){
	$routeProvider.when("/pessoas", {
		templateUrl : "views/bus.html",
		controller : "busController",
        access: { requiredLogin: false }
	});
});