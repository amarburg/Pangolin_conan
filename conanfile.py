from conans import ConanFile, CMake
import os

class PangolinConan(ConanFile):
  name = "pangolin"
  version = "master"
  url = "https://github.com/amarburg/Pangolin_conan.git"
  settings = "os", "compiler", "build_type", "arch"
  options = {"shared": [True, False], "build_parallel": [True, False]}
  default_options = "shared=True", "build_parallel=True"

  def source(self):
    if os.path.isdir('pangolin'):
      self.run('cd pangolin && git pull origin master')
    else:
      self.run('git clone https://github.com/stevenlovegrove/Pangolin pangolin')

  def build(self):
    cmake = CMake(self.settings)
    cmake_opts = "-DFORCE_GLUT=True "
    cmake_opts += "-DBUILD_SHARED_LIBS=True" if self.options.shared else ""

    if self.options.build_parallel:
      build_opts = "-- -j"
    self.run('cmake "%s/pangolin" %s %s' % (self.conanfile_directory, cmake.command_line, cmake_opts ))
    self.run('cmake --build . %s' % cmake.build_config)

  def package(self):
    self.copy("*.h", src="pangolin/include/", dst="include/")
    self.copy("*.hpp", src="pangolin/include/", dst="include/")
    self.copy("*.h", src="src/include/", dst="include/")
    if self.options.shared:
      if self.settings.os == "Macos":
          self.copy(pattern="*.dylib", dst="lib", keep_path=False)
      else:
          self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
    else:
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)

  def package_info(self):
      self.cpp_info.libs = ["pangolin"]
