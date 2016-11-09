
task :default => "debug:test"

@build_opts = {}
load 'config.rb' if FileTest::exists? 'config.rb'

['Debug','Release'].each { |build_type|
  namespace build_type.downcase.to_sym do
    build_dir = ENV['BUILD_DIR'] || "build-#{build_type}"

    task :build do
      FileUtils::mkdir build_dir unless FileTest::directory? build_dir

      cmake_opts = ["-o shared=True"]

      sh "conan source ."

      chdir build_dir do
        sh "conan install -s build_type=%s %s .. --build=missing" % [build_type, cmake_opts.join(' ')]
        sh "conan build .."
      end
    end

    task :test => :build do
      chdir build_dir do
      #sh "make unit_test"
    end
    end

  end
}

namespace :conan do
  task :export do
    sh "rm -rf build-*"
    sh "conan export amarburg/testing"
  end

  task :upload do
    sh "conan upload g2o/master@amarburg/testing"
  end
end

namespace :dependencies do

  task :trusty do
    sh "sudo apt-get install -y cmake libglew-dev"
    sh "pip install conan"
  end

  task :osx do
    sh "brew update"
    # sh "brew tap homebrew/science"
    sh "brew install glew conan"
  end

  namespace :travis do
    task :linux => "dependencies:trusty"
    task :osx => "dependencies:osx" do
      ## Technically the compiler version should be taken from Travis.yml is known
      File.open("~/.conan/conan.conf",'w') { |f|
        f.write <<CONAN_CONF_END
[settings_defaults]
arch=x86_64
build_type=Release
compiler=apple-clang
compiler.libcxx=libc++
compiler.version=7.3
os=Macos
CONAN_CONF_END
        }
      end
    end
  end
end
