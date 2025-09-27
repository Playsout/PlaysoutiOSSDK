#
# Be sure to run `pod lib lint PlaysoutiOSPod.podspec' to ensure this is a
# valid spec before submitting.
#
# Any lines starting with a # are optional, but their use is encouraged
# To learn more about a Podspec see https://guides.cocoapods.org/syntax/podspec.html
#

Pod::Spec.new do |s|
  s.name             = 'PlaysoutiOSPod'
  s.version          = '0.1.0'
  s.summary          = 'PlaysoutiOSPod is Playsout engine SDK for iOS Pod'

# This description is used to generate tags and improve search results.
#   * Think: What does it do? Why did you write it? What is the focus?
#   * Try to keep it short, snappy and to the point.
#   * Write the description between the DESC delimiters below.
#   * Finally, don't worry about the indent, CocoaPods strips it!

  s.description      = <<-DESC
TODO: Add long description of the pod here.
                       DESC

  s.homepage         = 'https://github.com/Playsout/PlaysoutiOSPod'
  # s.screenshots     = 'www.example.com/screenshots_1', 'www.example.com/screenshots_2'
  s.license          = { :type => 'MIT', :file => 'LICENSE' }
  s.author           = { 'Playsout' => '54703084+lkbtboy@users.noreply.github.com' }
  s.source           = { :git => 'https://github.com/Playsout/PlaysoutiOSPod.git', :tag => s.version.to_s }
  # s.social_media_url = 'https://twitter.com/Playsout'

  s.ios.deployment_target = '16.0'

  #s.source_files = 'PlaysoutiOSPod/Classes/**/*'

  s.framework  = "Foundation"
  s.static_framework = true
  
  s.ios.vendored_frameworks = 'ios_frameworks/*.xcframework'
  
  
  # s.resource_bundles = {
  #   'PlaysoutiOSPod' => ['PlaysoutiOSPod/Assets/*.png']
  # }

  # s.public_header_files = 'Pod/Classes/**/*.h'
  # s.frameworks = 'UIKit', 'MapKit'
  # s.dependency 'AFNetworking', '~> 2.3'
end
