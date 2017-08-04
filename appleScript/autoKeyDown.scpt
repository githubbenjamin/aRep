activate application "TextEdit"
delay 1
tell application "System Events"
	repeat with i from 1 to 51
		repeat with j from 1 to (random number from 2 to 8)
			key code (random number from 0 to 35)
			
		end repeat
		key code 36
    delay 0.1
	end repeat
	--key code 53
	--keystroke 53 --"h" using {command down}
end tell
