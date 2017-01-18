package main

import (
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"strings"
	//	"time"
)

//func runShell(cmdStr string) {
//	cmd := exec.Command("/bin/sh", "-c", cmdStr)
//	stdout, err := cmd.Output()
//	if err != nil {
//		println(err.Error())
//		return
//	}
//	print(string(stdout))
//}

//func xcodeBuild(para string) {
//	paraSet := map(string)string{
//		"list":"-list"
//		"target":""
//		"allTarget":""
//	}
//	cmd := exec.Command("/usr/bin/xcodebuild", para)
//}

type TagString struct {
	VarName string `xml:"varName,attr"`
	Value   string `xml:",chardata"`
}

//type TagStringList struct {
//	varName string `xml:"varName,attr"`
//	Value   string `xml:",chardata"`
//}

type PropertyListStruct struct {
	VarName   string      `xml:"varName,attr"`
	IsManaged string      `xml:"IsManaged,attr"`
	KeyString []TagString `xml:"String"`
	Bool      []string
	Int       []string
}

type PropertyLists struct {
	//	XMLName             xml.Name       `xml:"PropertyList"` // 一般建议根元素加上此字段
	PropertyListStructs []PropertyListStruct `xml:"PropertyList"`
	//	Strings []string `xml:"PropertyList>String"` // 规则 7，可见字段名可以随意

}

type P4VConnection struct {
	Name          string /*`xml:"varName"`*/
	User          string
	ServerAddress string
	P4Port        string
}

type P4VConnections struct {
	XMLName     xml.Name        `xml:"ConnectionMapList"`
	Connections []P4VConnection `xml:"ConnectionMap"`
}

type P4VClients struct {
	XMLName xml.Name `xml:"PropertyList"`
	//	StringLists []TagStringList `xml:"StringList"`
	TagStrings []TagString `xml:"String"`
}

type HostProperties struct {
	XMLName xml.Name `xml:HostProperties"`
	//	TagLists []TagList `xml:"tagList"`
	Tags []Tag `xml:"tag"`
}

type Tag struct {
	Key   string `xml:"name,attr"`
	Value string `xml:",chardata"`
}

func p4vAnchorName() string {
	//os.Getenv("BAR")
	//	p4vSFile := os.Getenv("HOME") + "/Library/Preferences/com.perforce.p4v/ApplicationSettings.xml"
	//	fmt.Printf("p4vSFile: %s", p4vSFile)
	p4vSFile := os.Getenv("HOME") + "/Library/Preferences/com.perforce.p4v/ApplicationSettings.xml"
	//	log.Printf(p4vSFile)
	//  /Users/gdlocal/Desktop/ApplicationSettings.xml
	//  /Users/gdlocal/Library/Preferences/com.perforce.p4v/ApplicationSettings.xml
	p4vSFileContent, err := ioutil.ReadFile(p4vSFile)
	if err != nil {
		log.Printf("%s", err)
		return ""
	}
	var p4vSFileResult PropertyLists
	err = xml.Unmarshal(p4vSFileContent, &p4vSFileResult)
	if err != nil {
		log.Printf("%s", err)
		return ""
	}
	//	log.Println(p4vSFileResult.PropertyListStructs[0].KeyString[2].varName)
	//	log.Println(len(p4vSFileResult.PropertyListStructs))
	lastConnection := []string{}
	for _, propertyList := range p4vSFileResult.PropertyListStructs {
		if propertyList.VarName == "Connection" {
			for _, tagString := range propertyList.KeyString {
				if tagString.VarName == "LastConnection" {
					lastConnection = strings.Split(tagString.Value, ", ")[:]
				}
			}
		}
	}

	//	log.Printf("lastConnection:%q", lastConnection)
	if len(lastConnection) == 0 {
		log.Printf("Get last connection failure")
		return ""
	}

	p4vCMFile := os.Getenv("HOME") + "/Library/Preferences/com.perforce.p4v/connectionmap.xml"
	var p4vCM P4VConnections
	p4vCMFileContent, err := ioutil.ReadFile(p4vCMFile)
	if err != nil {
		log.Printf("%s", err)
		return ""
	}

	err = xml.Unmarshal(p4vCMFileContent, &p4vCM)
	if err != nil {
		log.Printf("%s", err)
		return ""
	}

	var curClientName string
	for _, connct := range p4vCM.Connections {
		if connct.P4Port == lastConnection[0] && connct.User == lastConnection[1] {
			curClientName = connct.Name[:]
		}

	}
	//	log.Printf("current client name: %s", curClientName)
	if len(curClientName) == 0 {
		log.Printf("Get current client name failure")
		return ""
	}

	p4vCFFile := os.Getenv("HOME") + "/Library/Preferences/com.perforce.p4v/" + curClientName + "Clients/filters.xml"
	p4vCF := new(P4VClients)
	p4vCFFileContent, err := ioutil.ReadFile(p4vCFFile)
	//	log.Printf("p4vCFFileContent:%s", p4vCFFileContent)
	if err != nil {
		log.Printf("%s", err)
		return ""
	}

	err = xml.Unmarshal(p4vCFFileContent, &p4vCF)
	if err != nil {
		log.Printf("%s", err)
		return ""
	}
	var lastP4vLocalPath string

	for _, tag := range p4vCF.TagStrings {
		theKey := strings.Join([]string{"lastused_dashboard_filters", lastConnection[2]}, "")
		//		log.Printf("the key:%s", theKey)
		if tag.VarName == theKey {
			lastP4vLocalPath = tag.Value
		}
	}
	//	log.Printf("lastP4vLocalPath:%s", lastP4vLocalPath)
	if len(lastP4vLocalPath) == 0 {
		log.Printf("Get P4V local path failure")
		return ""
	}
	//	log.Printf("lastP4vLocalPath:%s", lastP4vLocalPath)
	return lastP4vLocalPath
}

func runShell(cmdString string) string {
	//	go run()
	//	time.Sleep(1e9)

	//	cmd := exec.Command("/bin/sh", "-c", `mobdev list 2>&1`)
	//	cmd := exec.Command("/usr/bin/mobdev", "-l", "0x24100000", "get", "NULL", "SerialNumber")
	cmd := exec.Command("/bin/sh", "-c", cmdString)
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Println("StdoutPipe: " + err.Error())
		return ""
	}

	stderr, err := cmd.StderrPipe()
	if err != nil {
		fmt.Println("StderrPipe: ", err.Error())
		return ""
	}

	if err := cmd.Start(); err != nil {
		fmt.Println("Start: ", err.Error())
		return ""
	}

	bytesErr, err := ioutil.ReadAll(stderr)
	if err != nil {
		fmt.Println("ReadAll stderr: ", err.Error())
		return ""
	}

	if len(bytesErr) != 0 {
		fmt.Printf("stderr is not nil: %s", bytesErr)
		return ""
	}

	bytes, err := ioutil.ReadAll(stdout)
	if err != nil {
		fmt.Println("ReadAll stdout: ", err.Error())
		return ""
	}

	if err := cmd.Wait(); err != nil {
		fmt.Println("Wait: ", err.Error())
		return ""
	}

	//	fmt.Printf("stdout: %s", bytes)
	return string(bytes)
}

func contains(slice []string, item string) bool {
	set := make(map[string]struct{}, len(slice))
	for _, s := range slice {
		set[s] = struct{}{}
	}

	_, ok := set[item]
	return ok
}

func main() {
	log.Print("start")
	//	args := os.Args
	//		fmt.Printf("argu:%s, arg len:%d\n", args, len(args))
	var p4vPath = p4vAnchorName()
	//	log.Printf("P4v path: %s", p4vPath)
	if p4vPath == "" {
		log.Printf("get p4v path failure")
		os.Exit(1)
	}

	//  /Users/gdlocal/Perforce/benjamin_seagull_290/StationSoftware/OpenTF-II/Framework/4-Code/OpenTF/OpenTF.xcodeproj
	openTFProject := p4vPath + "/StationSoftware/OpenTF-II/Framework/4-Code/OpenTF/OpenTF.xcodeproj"
	log.Printf("OpenTF project: %s", openTFProject)
	//	log.Printf("opentTF project path: %s", openTFProject)
	//	cmd := exec.Command("/usr/bin/xcodebuild", "-project", openTFProject, "-list")
	cmdStr := "xcodebuild -project \"" + openTFProject + "\" -list"
	//	log.Printf("cmd string: %s", cmdStr)

	//	fmt.Printf("stdout 0: %s", otfTargets)
	otfTargets2 := strings.Split(runShell(cmdStr), "Targets:")[1]
	otfTargets3 := strings.Split(otfTargets2, "Build Configurations:")[0]

	//	log.Printf("targets:\n%q", otfTargets3)
	//	proJctTargets := strings.Split(otfTargets3, "\n")

	proJctTargets := []string{}
	//	proJctTargets := new([]string)
	for _, targetName := range strings.Split(otfTargets3, "\n") {
		temp := strings.TrimSpace(targetName)
		//		log.Printf("%d, %q", len(temp), temp)
		if len(temp) != 0 {
			proJctTargets = append(proJctTargets, string(temp))
		}

	}
	//	proJctTargets
	log.Printf("targets:\n%q", proJctTargets)
	//	return
	//

	//-alltargets clean -configuration Release
	//cleanStart
	runShell("xcodebuild -project \"" + openTFProject + "\" -alltargets clean -configuration Release")

	runShell("xcodebuild -project \"" + openTFProject + "\" -alltargets build -configuration Release")

	// build the openTF base libs
	oftLibs := []string{"DDLog", "Configure", "libPrivateuSleep", "libQuerySFCByURL", "ParameterStruct", "libORSSerialPort"}
	//	for _, target := range oftLibs {

	//		command := "xcodebuild -project \"" + openTFProject + "\" -target " + target + " -configuration Release"
	//		log.Print(command)
	//		runShell(command)
	//	}

	// build the all dylib
	//	for _, target := range proJctTargets {
	//		if target == "OpenTF" {
	//			continue
	//		}
	//		if contains(oftLibs, target) {
	//			continue
	//		}
	//		command := "xcodebuild -project \"" + openTFProject + "\" -target " + target + " -configuration Release"
	//		log.Print(command)
	//		runShell(command)
	//		//		log.Printf("rst:%d", rst_cmd)
	//	}
	//	command := "xcodebuild -project \"" + openTFProject + "\" -target OpenTF -configuration Release"
	//	runShell(command)
	//	log.Printf("rst:%d", rst_cmd)

	buildPath := p4vPath + "/StationSoftware/OpenTF-II/Framework/4-Code/OpenTF/build/Release"
	os.Chdir(buildPath)
	//	otfFolders := []string{"pluginDylib", "lib", "bin"}
	os.MkdirAll("00_INSTALLPACKAGE/InstallOpenTF/OpenTFVersion/pluginDylib", 0755)
	os.MkdirAll("00_INSTALLPACKAGE/InstallOpenTF/OpenTFVersion/lib", 0755)
	os.MkdirAll("00_INSTALLPACKAGE/InstallOpenTF/OpenTFVersion/DeviceDriver", 0755)
	//  DeviceDriver

	//	os.Chdir("00_INSTALLPACKAGE/InstallOpenTF/OpenTFVersion/")
	runShell("cd \"" + buildPath + "\";cp *.dylib 00_INSTALLPACKAGE/InstallOpenTF/OpenTFVersion/pluginDylib/")
	//	oftLibs := []string{"Configure", "DDLog", "libPrivateuSleep", "libQuerySFCByURL", "ParameterStruct"}

	os.Chdir("00_INSTALLPACKAGE/InstallOpenTF/OpenTFVersion/pluginDylib/")
	for _, libName := range oftLibs {
		runShell("mv " + libName + ".dylib ../lib/")
	}
	runShell("mv libDrvUARTDevice.dylib ../DeviceDriver/")
	log.Println("finish.")
	runShell("open \"" + buildPath + "\"")

}
