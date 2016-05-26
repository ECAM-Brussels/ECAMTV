<div id="weather" class="widget">
	<div>
		% current = weather['current_condition']
		<div><img src="{{current['icon_big']}}" alt="Icon" /></div>
		<div>{{current['tmp']}}°</div>
		<div>{{current['condition']}}</div>
	</div>
	<div>
		<ul>
			% for i in range(4):
			%     forecast = weather['fcst_day_{}'.format(i)]
			<li>
				<div>{{forecast['day_short']}}</div>
				<div><img src="{{forecast['icon_big']}}" alt="Icon" /></div>
				<div>{{forecast['tmin']}}°/{{forecast['tmax']}}°</div>
			</li>
			% end
		</ul>
	</div>
</div>