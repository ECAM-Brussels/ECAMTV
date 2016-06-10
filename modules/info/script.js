$(function() {
	var $info = $('#info');
	// Configure the info panes
	var panels = $info.find('> div');
	var current = 0;
	// Switch between the panes
	var switchPane = function() {
		$(panels[current]).fadeOut(function() {
			current = (current + 1) % panels.length;
			$(panels[current]).fadeIn();
			setTimeout(switchPane, 5000);
		});
	};
	setTimeout(switchPane, 5000);
});