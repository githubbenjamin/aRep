extern "C" {
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"
}

#ifdef LUA_EXPORTS
#define LUA_API __declspec(dllexport)
#else
#define LUA_API __declspec(dllimport)
#endif

extern "C" LUA_API int luaopen_myLib01(lua_State *L); //定义导出函数
