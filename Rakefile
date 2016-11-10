
task :default => "debug:test"

@conan_opts = {shared: 'True'}
load 'config.rb' if FileTest::exists? 'config.rb'

['Debug','Release'].each { |build_type|
  namespace build_type.downcase.to_sym do
    build_dir = ENV['BUILD_DIR'] || "build-#{build_type}"

    task :build do
      FileUtils::mkdir build_dir unless FileTest::directory? build_dir

      cmake_opts = @conan_opts.each_pair.map { |k,v| "-o #{k}=#{v}" }

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
      File.open("config.rb",'w') { |f|
        f.write <<CONAN_CONF_END
@conan_opts[:compiler] = 'apple-clang'
@conan_opts["compiler.version".to_sym] = '7.3'
@conan_opts["compil"][settings_defaults]
CONAN_CONF_END
        }
      end
   end

end
