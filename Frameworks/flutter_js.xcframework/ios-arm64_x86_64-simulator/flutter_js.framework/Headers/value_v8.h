#ifndef FLUTTER_JS_VALUE_V8_H
#define FLUTTER_JS_VALUE_V8_H

#include "../value.h"
#ifdef TARGET_OS_IOS
#include "../include_ios/v8.h"
#else
#include "../include/v8.h"
#endif

class V8Context;

class V8Value : public Value
{
public:
    V8Value(V8Context *ctx, const v8::Local<v8::Value> &value, bool isException = false);
    virtual ~V8Value() { value_.Reset(); }
    V8Value(const V8Value &) = delete;
    V8Value &operator=(const V8Value &) = delete;

    virtual Context *GetContext() const;
    virtual Value *Call(Value *thisValue, std::vector<Value *> &args);

    virtual Value *Duplicate();
    virtual std::string ToCString();
    virtual bool ToBoolean() const;
    virtual int ToInt() const;
    virtual double ToDouble() const;
    virtual uint8_t *GetArrayBuffer(size_t *psize);

    virtual int GetTag();
    virtual bool IsException();
    virtual bool IsNull();
    virtual bool IsUndefined();
    virtual bool IsNullOrUndefined();
    virtual bool IsString() const;
    virtual bool IsNumber() const;
    virtual bool IsBoolean() const;
    virtual bool IsFunction();
    virtual bool IsObject();
    virtual bool IsArray();
    virtual bool IsSet();
    virtual bool IsMap();
    virtual bool IsArrayBuffer();

    virtual uint32_t GetArrayLength();
    virtual Value *GetArrayIdx(uint32_t idx);

    virtual Value *GetProperty(std::string name);
    virtual int SetProperty(std::string key, Value *prop);
    virtual int SetPropertyIdx(uint32_t idx, Value *prop);

    virtual Value *GetOwnPropertyNames();

    v8::Global<v8::Value> &GetValue();

private:
    V8Context *ctx_;
    v8::Isolate *isolate_;
    v8::Global<v8::Value> value_;
    bool isException_;
};

#endif // FLUTTER_JS_VALUE_V8_H