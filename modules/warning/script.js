$(function() {
	var $warning = $('#warning > ul');
	// Configure the scrolling area
	var nbItems = $warning.find('li').length;
	var parentWidth = $warning.parent().css('width');
	parentWidth = parentWidth.substr(0, parentWidth.indexOf('px'));
	$warning.css('width', (nbItems * 100) + '%');
	// Shows the element and starts horizontal scrolling
	var scrollOnce = function() {
		$warning.css('margin-left', parentWidth + 'px');
		$warning.css('display', 'block');
		$warning.animate({marginLeft: '-' + (nbItems * parentWidth) + 'px'}, nbItems * 10000, function() {
			$warning.css('display', 'none');
			setTimeout(scrollOnce, 0);
		});
	};
	scrollOnce();
});