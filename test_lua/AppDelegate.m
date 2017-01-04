#import "AppDelegate.h"

#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"

@interface AppDelegate ()

@property (weak) IBOutlet NSWindow *window;
@end

@implementation AppDelegate

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
    
    L = luaL_newstate();
    
    /* 载入Lua基本库 */
    luaL_openlibs(L);
    /* 注册函数 */
    lua_register(L, "average", average);
    /* 运行脚本 */
    luaL_dofile(L, "avg.lua");
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
