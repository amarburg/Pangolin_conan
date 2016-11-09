from conans import ConanFile, CMake
import os

class PangolinConan(ConanFile):
  name = "pangolin"
  version = "master"
  url = "https://github.com/amarburg/Pangolin_conan.git"
  settings = "os", "compiler", "build_type", "arch"
  options = {"shared": [True, False]}
  default_options = "shared=True"

  def source(self):
    if os.path.isdir('pangolin'):
      self.run('git update pangolin')
    else:
      self.run('git clone https://github.com/stevenlovegrove/Pangolin pangolin')

  def build(self):
    cmake = CMake(self.settings)
    if self.options.shared:
      cmake_opts = "-DBUILD_SHARED_LIBS=True" 
    self.run('cmake "%s/pangolin" %s %s' % (self.conanfile_directory, cmake.command_line, cmake_opts ))
    self.run('cmake --build . %s' % cmake.build_config)

  def package(self):
    self.copy("*.h", dst="")
    if self.options.shared:
      if self.settings.os == "Macos":
          self.copy(pattern="*.dylib", dst="lib", keep_path=False)
      else:
          self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
    else:
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)

  # def package_info(self):
  #     self.cpp_info.libs = ["videoio"]
