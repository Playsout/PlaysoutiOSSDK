#ifndef FLUTTER_JS_CONTEXT_V8_H
#define FLUTTER_JS_CONTEXT_V8_H

#include "../context.h"
#ifdef TARGET_OS_IOS
#include "../include_ios/v8.h"
#else
#include "../include/v8.h"
#endif
#include "wasm3_v8.h"

void JsCallbackNotifyCompletion();

class V8Context : public Context
{
public:
    V8Context(v8::Isolate *isolate);
    virtual ~V8Context();
    virtual Value *RunScript(std::string code, std::string filename, int type);
    virtual Value *CallFunction(Value *funcValue, Value *thisValue, std::vector<Value *> &args);
    virtual Value *GetGlobalObject();
    virtual Value *DuplicateGlobalObject();
    virtual Value *NewObject();
    virtual Value *NewInt(int val);
    virtual Value *NewDouble(double val);
    virtual Value *NewBool(bool val);
    virtual Value *NewString(std::string val);
    virtual Value *NewArray();
    virtual Value *NewArrayBuffer(const uint8_t *buf, size_t len);
    virtual Value *NewException(std::string val);

    virtual bool SetProperty(Value *object, Value *key, Value *value);
    virtual Value *BindFunction(std::string name, JSCallback callback);

    v8::Isolate *GetIsolate() { return isolate_; }
    v8::Local<v8::Context> GetPersistentContext() { return context_persistent_.Get(isolate_); };

protected:
    void Wasm_Instance(const v8::FunctionCallbackInfo<v8::Value> &Info);
    void Wasm_MemoryBuffer(const v8::FunctionCallbackInfo<v8::Value> &Info);
    void Wasm_MemoryGrowth(const v8::FunctionCallbackInfo<v8::Value> &Info);
    void Wasm_Table_Get(const v8::FunctionCallbackInfo<v8::Value> &Info);

private:
    Value *ExceptionError(v8::TryCatch &try_catch,
                          v8::Isolate *iso,
                          v8::Local<v8::Context> ctx);

private:
    v8::Isolate *isolate_;
    v8::Persistent<v8::ObjectTemplate> global_persistent_;
    v8::Persistent<v8::Context> context_persistent_;

    std::vector<FunctionInfo *> func_registers_;

    Value *global_object_;

    // for wasm3
    WasmEnv *_wasmEnv;
};

#endif // FLUTTER_JS_CONTEXT_V8_H