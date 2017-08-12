(*
Auto Key Down

description: this script for Q-Time auto testing

version: 0.0.1

maybe you need
	1. modify delay time(s), the line is marked by "-- sleep time"
	2. modify repeat times, the line is marked by "-- repeat times"

*)

--(*
activate application "Q-Time"

delay 1
tell application "System Events"
	repeat with i from 1 to 501 -- repeat times
		repeat with j from 1 to (random number from 2 to 8)
			key code (random number from 11 to 23)
			
		end repeat
		key code 36
		set frontApp to (name of first process where it is frontmost)
		if "Q-Time" is equal to frontApp then
			--display dialog ("Finder was last in front")
		else
			display dialog ("not Q-Time")
			break
		end if
		delay 0.1 -- sleep time
	end repeat
	--key code 53
	--keystroke 53 --"h" using {command down}
end tell

--*)

