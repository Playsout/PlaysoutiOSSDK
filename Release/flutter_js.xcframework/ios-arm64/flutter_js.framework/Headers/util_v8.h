#ifndef FLUTTER_JS_UTIL_V8_H
#define FLUTTER_JS_UTIL_V8_H

#include <string>
#ifdef TARGET_OS_IOS
#include "../include_ios/v8.h"
#include "../include_ios/libplatform/libplatform.h"
#else
#include "../include/v8.h"
#include "../include/libplatform/libplatform.h"
#endif

class V8Utils
{
public:
    inline static v8::Local<v8::String> ToV8String(v8::Isolate *Isolate, const char *String)
    {
        return v8::String::NewFromUtf8(Isolate, String, v8::NewStringType::kNormal).ToLocalChecked();
    }
    inline static void ThrowException(v8::Isolate *Isolate, const char *Message)
    {
        //auto ExceptionStr = v8::String::NewFromUtf8(Isolate, Message, v8::NewStringType::kNormal).ToLocalChecked();
        //Isolate->ThrowException(v8::Exception::Error(ExceptionStr));
    }
    inline static std::string TryCatchToString(v8::Isolate *Isolate, v8::TryCatch *TryCatch)
    {
        //return "";
        
        v8::Isolate::Scope IsolateScope(Isolate);
        v8::HandleScope HandleScope(Isolate);
        v8::String::Utf8Value Exception(Isolate, TryCatch->Exception());
        std::string ExceptionStr;
        if (Exception.length() > 0)
        {
            ExceptionStr = ((*Exception));
        }
        v8::Local<v8::Message> Message = TryCatch->Message();
        if (Message.IsEmpty())
        {
            // 如果没有提供更详细的信息，直接输出Exception
            return ExceptionStr;
        }
        else
        {
            v8::Local<v8::Context> Context(Isolate->GetCurrentContext());

            // 输出调用栈信息
            v8::Local<v8::Value> StackTrace;
            if (TryCatch->StackTrace(Context).ToLocal(&StackTrace))
            {
                v8::String::Utf8Value StackTraceVal(Isolate, StackTrace);
                std::string StackTraceStr(*StackTraceVal);
                ExceptionStr.append("\n").append(StackTraceStr);
                // ExceptionStr.Append("\n").Append(StackTraceStr);
            }
            else
            {
                // (filename:line:number).
                v8::String::Utf8Value FileName(Isolate, Message->GetScriptResourceName());
                std::string FileInfoStr = "(";
                FileInfoStr.append(*FileName);
                int LineNum = Message->GetLineNumber(Context).FromJust();
                int StartColumn = Message->GetStartColumn();
                FileInfoStr.append(":")
                    //.append(itoa(LineNum))
                    .append(": ")
                    //.append(FString::FromInt(StartColumn))
                    .append(")");

                ExceptionStr.append(" at ").append(FileInfoStr).append("\n");
            }
            return ExceptionStr;
        }
        
    }
};

#endif // FLUTTER_JS_VALUE_V8_H
