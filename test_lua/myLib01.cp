#include "myLib01.h"
#include <stdio.h>


static int averageFunc(lua_State *L)
{
    int n = lua_gettop(L);
    double sum = 0;
    int i;
    
    /* 循环求参数之和 */
    for (i = 1; i <= n; i++)
        sum += lua_tonumber(L, i);
    
    lua_pushnumber(L, sum / n);		//压入平均值
    lua_pushnumber(L, sum);			//压入和
    
    return 2;                       //返回两个结果
}

static int sayHelloFunc(lua_State* L)
{
    printf("hello world!");
    return 0;
}

static const struct luaL_Reg myLib[] =
{
    {"average", averageFunc},
    {"sayHello", sayHelloFunc},
    {NULL, NULL}       //数组中最后一对必须是{NULL, NULL}，用来表示结束
};

int luaopen_myLib01(lua_State *L)
{
    const luaL_Reg* libf =myLib;
    for (; libf->func; libf++)
    {
        //把foo函数注册进lua，第二个参数代表Lua中要调用的函数名称，第三个参数就是c层的函数名称
        lua_register(L,libf->name,libf->func);
        //将栈顶清空
        lua_settop(L,0);
    }
    
//    luaL_register(L, "ss", myLib);
    return 1;		// 把myLib表压入了栈中，所以就需要返回1
}
