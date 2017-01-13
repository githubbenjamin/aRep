#import "AppDelegate.h"

#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"
#include "lua_cjson.h"



@interface AppDelegate ()

@property (weak) IBOutlet NSWindow *window;
@end

@implementation AppDelegate

static int socketManneger(lua_State *L)
{
    /* load lua socket */
    luaopen_socket_core(L);
    return 1;
}

lua_State* L;
static int average(lua_State *L)
{
    /* 得到参数个数 */
    int n = lua_gettop(L);
    double sum = 0;
    int i;
    
    /* 循环求参数之和 */
    for (i = 1; i <= n; i++)
    {
        /* 求和 */
        sum += lua_tonumber(L, i);
    }
    /* 压入平均值 */
    lua_pushnumber(L, sum / n);
    /* 压入和 */
    lua_pushnumber(L, sum);
    /* 返回返回值的个数 */
    return 2;
}

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
    // Insert code here to initialize your application
    [self test];
    NSMutableArray* ma = [NSMutableArray new];
    [ma lastObject];
    [ma removeLastObject];
    
    L = luaL_newstate();
    
    /* 载入Lua基本库 */
    luaL_openlibs(L);
    
//    lua_register(L, "socketInstance", socketManneger);
//     luaL_newlib(L, mathlib);
//    luaL_requiref(L, "socket", luaopen_socket_core, 1);
//
    luaopen_socket_core(L);
    lua_pushvalue(L, -1);  /* copy of module */
    lua_setglobal(L, "socket");  /* _G[modname] = module */
    //lua_pop(L, 1);
    
    luaopen_cjson(L);
    /* 注册函数 */
    lua_register(L, "average", average);
    /* 运行脚本 */
    int rst = luaL_dofile(L, "main.lua");
    if (rst != LUA_OK) {
        //CallInfo *ci = L->ci;
        printf("error\n");//ci->u.c.ctx);
    }
    /* 清除Lua */
    lua_close(L);
    
    /* 暂停 */
    printf( "Press enter to exit…" );
    getchar();
}

- (void)applicationWillTerminate:(NSNotification *)aNotification {
    // Insert code here to tear down your application
}

@end
