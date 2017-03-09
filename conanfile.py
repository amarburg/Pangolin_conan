from conans import ConanFile, CMake, tools
import os

class PangolinConan(ConanFile):
  name = "pangolin"
  version = "master"
  url = "https://github.com/amarburg/Pangolin_conan.git"
  source_url = "https://github.com/stevenlovegrove/Pangolin.git"
  commit = "master"
  settings = "os", "compiler", "build_type", "arch"
  options = {"shared": [True, False], "build_parallel": [True, False]}
  default_options = "shared=True", "build_parallel=True"

  def source(self):
    if not os.path.isdir('pangolin'):
      self.run('git clone %s pangolin' % self.source_url)
    else:
      self.run('cd pangolin && git fetch origin')

    self.run('cd pangolin && git checkout %s' % self.commit)

    if self.settings.os == "Macos":
        tools.patch(patch_file="file.patch") ../patches/squelch_error_1280.patch')

  def build(self):
    cmake = CMake(self.settings)

    cmake_opts = " -DBUILD_EXAMPLES:BOOL=False"
    cmake_opts += " -DBUILD_TESTS:BOOL=False"
    cmake_opts += " -DBUILD_SHARED_LIBS=True" if self.options.shared else ""

    if self.options.build_parallel:
      build_opts = "-- -j"

    ## Explicitly disable RPATH on OSX
    if self.settings.os == "Macos":
      cmake_opts += " -DCMAKE_SKIP_RPATH:BOOL=ON"

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
          self.copy(pattern="*.so*", dst="lib", keep_path=False)
    else:
        self.copy(pattern="*.a", dst="lib", keep_path=False)

  def package_info(self):
      self.cpp_info.libs = ["pangolin"]
