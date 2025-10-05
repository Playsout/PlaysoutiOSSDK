
#ifndef FLUTTER_JS_RUNTIME_V8_H
#define FLUTTER_JS_RUNTIME_V8_H

#ifdef TARGET_OS_IOS
#include "../include_ios/v8.h"
#else
#include "../include/v8.h"
#endif
#include "../runtime.h"

class V8Runtime : public Runtime
{
public:
    V8Runtime();
    virtual ~V8Runtime();
    virtual Context *CreateContext();
    virtual bool ExecutePendingJob();
    virtual void TriggerGC();

private:
    v8::Isolate *isolate_;
    v8::Isolate::CreateParams create_params_;
};

#endif // FLUTTER_JS_RUNTIME_H