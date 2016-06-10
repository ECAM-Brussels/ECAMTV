<div id="transport" class="widget">
	% for waitingtime in schedule:
	%     for line in waitingtime:
	%         for destination in waitingtime[line]:
	<div>
		<div><span class="line{{line}}">{{line}}</span> {{destination}}</div>
		<div>
	%             for minute in waitingtime[line][destination]:
			<span>{{minute}}</span>
	%             end
		</div>
	</div>
	%         end
	%     end
	% end
</div>