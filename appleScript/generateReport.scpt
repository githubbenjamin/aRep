-- This script helps generate IT data reports. 


global SNList

global ConfigList

global cnt



set SNList to {}

set ConfigList to {}

set cnt to 1

set found to ""





-- Get current folder path



set current_path to ""



tell application "Finder"
	
	set current_path to container of (path to me) as alias
	
end tell



-- Get SN file

set theFile to (current_path as text) & "Serial Number by Config:SN.xlsx"



-- Set SN by config output folder

set destFolder to (current_path as text) & "Serial Number by Config:"



-- Set SN by Config file name

set desSNFile to (destFolder as text) & "SNbyConfig.csv"











----------------------------------------

--Populate SN by config csv---

----------------------------------------



getSNbyConfig(theFile, desSNFile)



----------------------------------------

--Generate IT main overall data---

----------------------------------------



GenOverallData("IT_Main", "IT Main Raw Data", current_path)



----------------------------------------

--Generate IT SA overall data---

----------------------------------------



GenOverallData("IT_SA", "IT SA Raw Data", current_path)



on getSNbyConfig(sourceFile, destFile)
	
	
	
	tell application "Microsoft Excel"
		
		
		
		-- Get Excel to activate
		
		activate
		
		
		
		-- Close any workbooks that we have open
		
		close workbooks saving yes
		
		
		
		-- Ask Excel to open the theFile spreadsheet
		
		open sourceFile
		
		-- Set maxCount to the total number of sheets in this workbook
		
		set maxCount to count of worksheets of active workbook
		
		-- For each sheet in the workbook, loop through them one by one
		
		repeat with i from 1 to maxCount
			
			set sourceFile to active workbook
			
			-- Set the current worksheet to our loop position
			
			--Get config name from tabs
			
			set theWorksheetname to name of worksheet i of active workbook
			
			set theWorksheet to worksheet i of active workbook
			
			activate object theWorksheet
			
			--Grab all data from current sheet
			
			tell theWorksheet to set myData to value of used range
			
			repeat with m from 1 to count of myData
				
				set myContent to (item 1 of item m of myData) as text
				
				set myContent2 to theWorksheetname as text
				
				--ignore ISN header and empty line
				
				if (myContent ≠ "ISN" and myContent ≠ "") then
					
					--write serial code
					
					my write2file(destFile, myContent & "::")
					
					--write conrresponding config
					
					my write2file(destFile, myContent2 & return)
					
					set SNList to SNList & myContent
					
					set ConfigList to ConfigList & myContent2
					
				end if
				
			end repeat
			
			
			
		end repeat
		
		
		
		
		
		-- Close the worksheet that we've just created
		
		close active workbook
		
		-- Clean up and close files
		
		close workbooks
		
		
		
	end tell
	
end getSNbyConfig



---------------------------------------------------------------

--Copy SN by config data into yield excel template---

---------------------------------------------------------------



-- Copy SN by conig info into IT Main



-- Get IT Main file



on GenOverallData(machineName, rawDataFolder, currentPath)
	
	
	
	tell application "Microsoft Excel"
		
		
		
		-- Get Excel to activate
		
		activate
		
		
		
		make new workbook
		
		
		
		set overallFile to (currentPath as text) & "Reports:" & machineName & ".xlsx"
		
		--set theWorkbookName to name of (info for itMainFile) -- OPEN IT Main file
		
		
		
		tell active workbook
			
			save workbook as filename overallFile with overwrite
			
		end tell
		
		
		
		open overallFile
		
		
		
		set theWorkbook to active workbook
		
		
		
		-- Switch to SN_Config tab
		
		tell active workbook
			
			
			
			tell active sheet
				
				try
					
					set name to "SN_Config"
					
				on error
					
					
					
				end try
				
			end tell
			
			
			
		end tell
		
		
		
		
		
		
		
		-- Fill SN into SN_Config tab
		
		tell active sheet of theWorkbook
			
			
			
			set value of range "A1" to "Serial number"
			
			set value of range "B1" to "Config"
			
			repeat with n from 1 to length of SNList
				
				set value of range ("A" & (n + 1)) to item n of SNList
				
			end repeat
			
			
			
			
			
			
			
			-- Fill Config into SN_Config tab
			
			
			
			
			
			repeat with m from 1 to length of ConfigList
				
				set value of range ("B" & (m + 1)) to item m of ConfigList
				
			end repeat
			
		end tell
		
		tell active workbook
			
			set lastSheet to sheet "SN_Config"
			
		end tell
		
		
		-- Get all the files in IT main raw data folder and fill them into individual sheets of IT_Main excel
		
		set TID to AppleScript's text item delimiters
		
		set AppleScript's text item delimiters to ","
		
		
		--tell application "Finder" to set the_files to get every file of folder ((current_path as text) & "IT Main Raw Data")
		
		set file_names to (list folder ((currentPath as text) & rawDataFolder) without invisibles)
		
		repeat with m from 1 to count of file_names
			
			set originFile to (currentPath as text) & rawDataFolder & ":" & item m of file_names
			
			set csvText to read alias originFile as «class utf8»
			
			-- Grabs all the contents from CSV
			
			set myArray to paragraphs of csvText
			
			-- Create new work sheet with machine name        
			
			tell active workbook
				
				make new worksheet at beginning
				
				tell active sheet
					try
						
						set name to my getWord((item 2 of myArray), 1)
						
					on error
						
						set cnt to cnt + 1
						
						set name to (my getWord((item 2 of myArray), 1)) & "(" & cnt & ")"
						
					end try
					
				end tell
				
			end tell
			
			-- Fill data into tabs
			
			tell active sheet of theWorkbook
				
				repeat with i from 1 to count of myArray
					
					--set value of used range to item i of myArray
					
					repeat with n from 1 to my countWord(item i of myArray)
						
						set value of range (my excelColumnToLetters(n) & i) to my getWord((item i of myArray), n)
						
					end repeat
					
				end repeat
				
				
				--add config column
				
				insert into range column 3 of sheet 1
				
				set value of range "C1" to "Config"
				
				repeat with i from 2 to ((count of myArray) - 1)
					
					set value of range ("C" & i) to ("=VLOOKUP(B" & i & ",'SN_config'!A:B,2,FALSE)")
					
				end repeat
				
				--add bay
				
				insert into range column 1 of sheet 1
				
				set value of range "A1" to "Bay"
				
				repeat with i from 2 to ((count of myArray) - 1)
					
					set value of range ("A" & i) to my getBay(item m of file_names)
					
				end repeat
				
				--add Vendor
				
				insert into range column 2 of sheet 1
				
				set value of range "B1" to "Vendor"
				
				repeat with i from 2 to ((count of myArray) - 1)
					
					set value of range ("B" & i) to my getVendor(item m of file_names)
					
				end repeat
				
				--"Delete N/A rows"
				
				set countArray to count of myArray
				
				repeat with i from ((count of myArray) - 1) to 2 by -1
					
					set found to ""
					
					set searchRange to range ("E" & i) of active sheet
					
					--return value of range "E2"
					
					set searchInfo to "#N/A"
					
					try
						
						set found to find searchRange what searchInfo look at whole with match case
						
					on error
						
						set found to ""
						
					end try
					
					if found is not "" then
						
						delete row i
						
						set countArray to countArray - 1
						
					end if
					
				end repeat
				
				--Delete duplicate rows
				
				set pnt to 2
				
				repeat while (value of range ("D" & pnt)) is not ""
					
					if value of range ("D" & pnt) = value of range ("D" & (pnt + 1)) then
						
						delete row pnt
						
					else
						
						set pnt to pnt + 1
						
					end if
					
					
					
				end repeat
				
				set cnt to 1
				
				
				
			end tell
			
			
			
			
			
			
			
		end repeat
		
		
		
		--add bay and vendor info column
		
		close active workbook saving yes
		
		
		
	end tell
	
	
	
end GenOverallData

























on getWord(thisText, id)
	
	
	
	set tempText to thisText
	
	
	
	
	
	
	
	if id > 1 then
		
		repeat with i from 1 to (id - 1)
			
			set tempText to text ((offset of "," in tempText) + 1) thru (length of tempText) of tempText
			
		end repeat
		
	end if
	
	
	
	if text 1 of tempText = "," then
		
		return ""
		
	end if
	
	
	
	
	
	return text 1 thru ((offset of "," in tempText) - 1) of tempText
	
	
	
	
	
end getWord





on countWord(thisText)
	
	
	
	set tempText to thisText
	
	set cnum to 1
	
	
	
	repeat while (tempText contains ",")
		
		set cnum to cnum + 1
		
		set tempText to text ((offset of "," in tempText) + 1) thru (length of tempText) of tempText
		
	end repeat
	
	
	
	if tempText = "" then
		
		set cnum to 0
		
	end if
	
	return cnum
	
	
	
end countWord





--Write function definition

on write2file(thisFile, thisText)
	
	try
		
		open for access file the thisFile with write permission
		
		write (thisText) to file the thisFile starting at eof
		
		close access file the thisFile
		
	on error
		
		try
			
			close access file the thisFile
			
		end try
		
	end try
	
end write2file



-- Create excel 

on createExcel(thisName)
	
	tell application "Microsoft Excel"
		
		set newWorkbook to make new workbook
		
		save workbook as newWorkbook filename thisName with overwrite
		
		set newWorkbook to active workbook
		
		close active workbook
		
	end tell
	
	
	
end createExcel



-- converts the column number to the letter equivalent

to excelColumnToLetters(column)
	
	set letters to {}
	
	repeat while column > 0
		
		set remainder to column mod 26
		
		if remainder = 0 then set remainder to 26
		
		set beginning of letters to (remainder + 64)
		
		set column to (column - remainder) div 26
		
	end repeat
	
	return string id letters
	
end excelColumnToLetters


on getVendor(thisText)
	
	return word 3 of thisText
	
end getVendor


on getBay(thisText)
	
	return word 6 of thisText
	
end getBay

