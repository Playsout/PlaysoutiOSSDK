#ifndef FLUTTER_JS_WASM3_V8_H
#define FLUTTER_JS_WASM3_V8_H

#include <functional>
#pragma warning(push, 0)
//#include "include/libplatform/libplatform.h"
#ifdef TARGET_OS_IOS
#include "../include_ios/v8.h"
#else
#include "../include/v8.h"
#endif
#pragma warning(pop)
#include "../wasm3/m3_api_wasi.h"
#include "../wasm3/wasm3.h"
#include "../wasm3/m3_env.h"

#define M3_FUNCTION_KEY "__playsout_inner_m3_func"

struct WasmNormalLinkInfo
{
    v8::UniquePersistent<v8::Function> CachedFunction;
    v8::Isolate *Isolate;
};

class WasmEnv
{
public:
    WasmEnv();
    ~WasmEnv();
    IM3Environment GetEnv()
    {
        return _Env;
    }

private:
    IM3Environment _Env;
};

/*
typedef bool (*WasmStaticLinkClassFunction)(IM3Module _Module);

class WasmStaticLinkClass
{
public:
    WasmStaticLinkClass(WasmStaticLinkClassFunction func, int Category);

    static bool Link(IM3Module _Module, int Category);
};
*/
class WasmRuntime;

using AdditionLinkFunc = std::function<bool(IM3Module)>;

class WasmModuleInstance
{
public:
    WasmModuleInstance(void *Buffer, int BufferLength);
    ~WasmModuleInstance();
    IM3Module GetModule()
    {
        return _Module;
    }
    uint32_t TableSize() const;
    bool TableGet(size_t Idx, IM3Function *Function);
    void TableSet(size_t Idx, IM3Function Function) const;
    bool ParseModule(WasmEnv *Env);
    bool LoadModule(WasmRuntime *Runtime, int LinkCategory, AdditionLinkFunc _Func = nullptr);
    int Index = -1;

private:
    void freeData();

private:
    IM3Module _Module;
    // std::map<>
    struct
    {
        uint8_t *bytes;
        size_t size;
    } data;
};

class WasmRuntime
{
public:
    WasmRuntime(WasmEnv *Env, int MaxPage = 1024, int InitPage = 64, int StackSizeInBytes = 256 * 1024);
    ~WasmRuntime();

    WasmEnv *GetEnv()
    {
        return _Env;
    }

    IM3Runtime GetRuntime() const
    {
        return _Runtime;
    }

    int Grow(int number);
    uint8_t *GetBuffer(int &Length);

    uint16_t GetRuntimeSeq() const
    {
        return _RuntimeSeq;
    }

    WasmModuleInstance *GetModuleInstance(int index) const
    {
        return _AllModuleInstances[index];
    }

    WasmModuleInstance *OnModuleInstance(WasmModuleInstance *InModuleInstance);

private:
    WasmEnv *_Env;
    IM3Runtime _Runtime;
    std::vector<WasmModuleInstance *> _AllModuleInstances;
    uint16_t _RuntimeSeq;
};

WasmRuntime *GetWasmRuntime(uint16_t seq);
void Wasm3InstanceCall(const v8::FunctionCallbackInfo<v8::Value> &Info);
WasmRuntime *Wasm3InstanceModule(WasmEnv *Env, v8::Isolate *Isolate, v8::Local<v8::Context> &Context, void *Buffer, int BufferLength,
                                 v8::Local<v8::Object> &ExportsObject, v8::Local<v8::Value> ImportsValue);

#endif // FLUTTER_JS_VALUE_V8_H