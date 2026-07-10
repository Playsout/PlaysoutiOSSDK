// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "PlaysoutSDK",
    platforms: [.iOS(.v16.0)],
    products: [
        .library(
            name: "PlaysoutSDK",
            targets: [
                "App"
                "FBLPromises"
                "FirebaseAnalytics"
                "FirebaseCore"
                "FirebaseCoreExtension"
                "FirebaseCoreInternal"
                "FirebaseCrashlytics"
                "FirebaseInstallations"
                "FirebaseRemoteConfigInterop"
                "FirebaseSessions"
                "Flutter"
                "FlutterPluginRegistrant"
                "GoogleAppMeasurement"
                "GoogleAppMeasurementIdentitySupport"
                "GoogleDataTransport"
                "GoogleMobileAds"
                "GoogleUtilities"
                "Google_Mobile_Ads_SDK"
                "KeychainAccess"
                "Promises"
                "SAMKeychain"
                "UserMessagingPlatform"
                "app_links"
                "audioplayers_darwin"
                "device_info_plus"
                "firebase_analytics"
                "firebase_core"
                "firebase_crashlytics"
                "flutter_image_api"
                "flutter_js"
                "flutter_udid"
                "flutter_webgl"
                "google_mobile_ads"
                "image_picker_ios"
                "in_app_purchase_storekit"
                "libEGL"
                "libGLESv2"
                "nanopb"
                "objective_c"
                "package_info_plus"
                "permission_handler_apple"
                "shared_preferences_foundation"
                "sqflite_darwin"
                "url_launcher_ios"
                "vibration"
                "wakelock_plus"
                "webview_flutter_wkwebview"
            ]
        )
    ],
    targets: [
        .binaryTarget(name: "App", path: "Frameworks/App.xcframework")
        .binaryTarget(name: "FBLPromises", path: "Frameworks/FBLPromises.xcframework")
        .binaryTarget(name: "FirebaseAnalytics", path: "Frameworks/FirebaseAnalytics.xcframework")
        .binaryTarget(name: "FirebaseCore", path: "Frameworks/FirebaseCore.xcframework")
        .binaryTarget(name: "FirebaseCoreExtension", path: "Frameworks/FirebaseCoreExtension.xcframework")
        .binaryTarget(name: "FirebaseCoreInternal", path: "Frameworks/FirebaseCoreInternal.xcframework")
        .binaryTarget(name: "FirebaseCrashlytics", path: "Frameworks/FirebaseCrashlytics.xcframework")
        .binaryTarget(name: "FirebaseInstallations", path: "Frameworks/FirebaseInstallations.xcframework")
        .binaryTarget(name: "FirebaseRemoteConfigInterop", path: "Frameworks/FirebaseRemoteConfigInterop.xcframework")
        .binaryTarget(name: "FirebaseSessions", path: "Frameworks/FirebaseSessions.xcframework")
        .binaryTarget(name: "Flutter", path: "Frameworks/Flutter.xcframework")
        .binaryTarget(name: "FlutterPluginRegistrant", path: "Frameworks/FlutterPluginRegistrant.xcframework")
        .binaryTarget(name: "GoogleAppMeasurement", path: "Frameworks/GoogleAppMeasurement.xcframework")
        .binaryTarget(name: "GoogleAppMeasurementIdentitySupport", path: "Frameworks/GoogleAppMeasurementIdentitySupport.xcframework")
        .binaryTarget(name: "GoogleDataTransport", path: "Frameworks/GoogleDataTransport.xcframework")
        .binaryTarget(name: "GoogleMobileAds", path: "Frameworks/GoogleMobileAds.xcframework")
        .binaryTarget(name: "GoogleUtilities", path: "Frameworks/GoogleUtilities.xcframework")
        .binaryTarget(name: "Google_Mobile_Ads_SDK", path: "Frameworks/Google_Mobile_Ads_SDK.xcframework")
        .binaryTarget(name: "KeychainAccess", path: "Frameworks/KeychainAccess.xcframework")
        .binaryTarget(name: "Promises", path: "Frameworks/Promises.xcframework")
        .binaryTarget(name: "SAMKeychain", path: "Frameworks/SAMKeychain.xcframework")
        .binaryTarget(name: "UserMessagingPlatform", path: "Frameworks/UserMessagingPlatform.xcframework")
        .binaryTarget(name: "app_links", path: "Frameworks/app_links.xcframework")
        .binaryTarget(name: "audioplayers_darwin", path: "Frameworks/audioplayers_darwin.xcframework")
        .binaryTarget(name: "device_info_plus", path: "Frameworks/device_info_plus.xcframework")
        .binaryTarget(name: "firebase_analytics", path: "Frameworks/firebase_analytics.xcframework")
        .binaryTarget(name: "firebase_core", path: "Frameworks/firebase_core.xcframework")
        .binaryTarget(name: "firebase_crashlytics", path: "Frameworks/firebase_crashlytics.xcframework")
        .binaryTarget(name: "flutter_image_api", path: "Frameworks/flutter_image_api.xcframework")
        .binaryTarget(name: "flutter_js", path: "Frameworks/flutter_js.xcframework")
        .binaryTarget(name: "flutter_udid", path: "Frameworks/flutter_udid.xcframework")
        .binaryTarget(name: "flutter_webgl", path: "Frameworks/flutter_webgl.xcframework")
        .binaryTarget(name: "google_mobile_ads", path: "Frameworks/google_mobile_ads.xcframework")
        .binaryTarget(name: "image_picker_ios", path: "Frameworks/image_picker_ios.xcframework")
        .binaryTarget(name: "in_app_purchase_storekit", path: "Frameworks/in_app_purchase_storekit.xcframework")
        .binaryTarget(name: "libEGL", path: "Frameworks/libEGL.xcframework")
        .binaryTarget(name: "libGLESv2", path: "Frameworks/libGLESv2.xcframework")
        .binaryTarget(name: "nanopb", path: "Frameworks/nanopb.xcframework")
        .binaryTarget(name: "objective_c", path: "Frameworks/objective_c.xcframework")
        .binaryTarget(name: "package_info_plus", path: "Frameworks/package_info_plus.xcframework")
        .binaryTarget(name: "permission_handler_apple", path: "Frameworks/permission_handler_apple.xcframework")
        .binaryTarget(name: "shared_preferences_foundation", path: "Frameworks/shared_preferences_foundation.xcframework")
        .binaryTarget(name: "sqflite_darwin", path: "Frameworks/sqflite_darwin.xcframework")
        .binaryTarget(name: "url_launcher_ios", path: "Frameworks/url_launcher_ios.xcframework")
        .binaryTarget(name: "vibration", path: "Frameworks/vibration.xcframework")
        .binaryTarget(name: "wakelock_plus", path: "Frameworks/wakelock_plus.xcframework")
        .binaryTarget(name: "webview_flutter_wkwebview", path: "Frameworks/webview_flutter_wkwebview.xcframework")
    ]
)
