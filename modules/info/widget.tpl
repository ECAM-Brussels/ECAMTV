<div id="info" class="widget">
	% for info in infos:
	<div>
		<div>{{info['title']}}</div>
		<div>{{!info['content']}}</div>
	</div>
	% end
</div>