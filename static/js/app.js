var formAppModule = angular.module('formApp', []);

formAppModule.config(function ($routeProvider) {
	$routeProvider.
	when('/', {controller: SignupController, templateUrl: 'static/signup.html'}).
	when('/enrollment', {controller: EnrollmentController, templateUrl: 'static/enrollment.html'});
	// .otherwise({redirectTo: '/'});
});


var SignupController = function ($scope, $location, $http) {
	$scope.thing = 1;
	$scope.hiddenButton = false;
	$scope.personal = {firstname: '', lastname: '', email: ''};
	// $scope.card = {'number': '', 'cvc': '', 'exp-month': '', 'exp-year': ''};
	$scope.errorMessage = '';
	Stripe.setPublishableKey('pk_test_eqBeMzmriQJ121FjtUtWMcO0');

	var stripeResponseHandler = function (status, response) {
		console.log('gots here too yo!');
		if (response.error) {
			console.log('unsuccess');
			$scope.errorMessage = response.error.message;
			$scope.hiddenButton = false;
		} else {
			console.log('successful transaction');
			var tok = response.id;
			console.log(tok);

			var personalform = document.getElementById('personal-form');
			console.log(personalform.firstname.value);

			$.ajax({
				type: 'GET',
				url: '/api/signup',
				data: {
					fname: personalform.firstname.value,
					lname: personalform.lastname.value,
					eml: personalform.email.value,
					tken: tok
				}
			});

			document.getElementById('errmess').innerHTML = '';

			$location.path('/enrollment');
		}
	};

	$scope.submit = function () {
		console.log('gots here yo!');
		$scope.hiddenButton = true;
		$scope.errorMessage = 'Processing...';

		var myForm = document.getElementById('payment-form')
		Stripe.createToken(myForm, stripeResponseHandler);
		console.log('Got after this call like a boss');
		if ($scope.errorMessage == '') {
			$location.path('/enrollment');
		}
	};
};

var EnrollmentController = function ($scope) {
	$scope.thing = 1;
};

formAppModule.directive('regexValidate', function () {
	return {
		restrict: 'A',
		require: 'ngModel',
		link: function (scope, elements, attributes, controller) {
			var re = new RegExp(attributes.regexValidate);
			controller.$parsers.unshift(function (value) {
				var valid = re.test(value);
				controller.$setValidity('regexValidate', valid);
				return valid ? value : undefined;
			});
			controller.$formatters.unshift(function (value) {
				controller.$setValidity('regexValidate', re.test(value));
				return value;
			});
		}
	};
});
