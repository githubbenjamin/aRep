--r1, r2 = average(3,4,5,6,7,9)
--print(r1, r2)

--[[
require "myLib01"
local ave,sum = ss.average(1,2,3,4,5) --参数对应堆栈中的数据
print(ave,sum)  -- 3 15
ss.sayHello()   -- hello world!
 
 ]]--

package.cpath = package.cpath .. ";?.dylib"
print(package.cpath)
rtn = require ("myLib01")
print(rtn)


local host, port = "127.0.0.1", 2942
local ss = assert(socket.tcp())
ss:bind(host, port)
ss:listen(3)
--[[
client = ss:accept()
client:send("get connect ok\n")
rc = client:receive("*l")
print("receive:"..rc)
]]

-- test the cjson
local json = cjson
local json_string = "{ \"name\":\"xiaoming\",\"age\":\"3\" }"
local tab = json.decode(json_string)
--print("tab->"..table.concat(tab, ",", 0,-1))

t2 = { ["first"]="first value", ["second"]="second value",["third"]="third value" }
t3 = { t2, {["a1"]="zz",["a2"]="nn"} }
--table.sort(t2)
for ii,vv in pairs(t3) do
for i, v in pairs(vv) do
print("tab:"..i.."->"..v)
end
end
--for i,v in ipairs(a) do print(i .. "->" ..v) end
--table.(tab, function(i, v) print(i.."->"..v)end)
json_string2 = json.encode(t3)
print("json string->"..json_string2)
