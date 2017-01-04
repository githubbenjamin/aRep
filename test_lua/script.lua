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
