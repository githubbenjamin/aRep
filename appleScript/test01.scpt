tell application "System Events"
	key code 53
	--keystroke 53 --"h" using {command down}
end tell

say "How are you?" using "Zarvox"
say "Fine, thank you." using "Victoria"
say "Ha Ha"
beep 1 --beep

set current_path to ""

tell application "Finder"
	set current_path to container of (path to me) as alias
end tell

--log current_path

set currentDate to current date
say "it's " & (currentDate's hours as text) & "" & (currentDate's minutes as text) using ""

display dialog "Hi there!" buttons {"Cancel", "OK", "Third Choose"} default button 2

set tempName to display dialog "Who is your favorite actress?" default answer "Julia"

(* multiline comment*)

tell application "iTunes"
	-- insert actions here
	
end tell
