$(function() {
	moment.locale('fr');
	setInterval(function() {
		var now = moment();
		$('#datetime > div:nth-child(1)').html(now.format('D MMMM YYYY'));
		$('#datetime > div:nth-child(2)').html(now.format('HH:mm'));
	}, 1000);
});