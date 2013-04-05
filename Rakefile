VERSION = "0.0.5"

def colorize(text, color)
  color_codes = {
    :black    => 30,
    :red      => 31,
    :green    => 32,
    :yellow   => 33,
    :blue     => 34,
    :magenta  => 35,
    :cyan     => 36,
    :white    => 37
  }
  code = color_codes[color]
  if code == nil
    text
  else
    "\033[#{code}m#{text}\033[0m"
  end
end

def virtual_env(command, env="env27")
  sh "source #{env}/bin/activate ; #{command}"
end

def create_virtual_env(dir, python)
  sh "virtualenv #{dir} -p #{python}"
  virtual_env("pip install -r requirements.txt")
  virtual_env("pip install -r requirements-test.txt")
end

task :dev_env => [] do
  create_virtual_env("env27", "python2.7")
  create_virtual_env("env32", "python3.2")
  create_virtual_env("env33", "python3.3")
end

task :tests => [] do
  virtual_env("nosetests", "env27")
  virtual_env("nosetests", "env32")
  virtual_env("nosetests", "env33")
end

task :tag => [:tests] do
  sh "git tag #{VERSION}"
  sh "git push origin #{VERSION}"
end

task :reset_tag => [] do
  sh "git tag -d #{VERSION}"
  sh "git push origin :refs/tags/#{VERSION}"
  sh "git tag #{VERSION}"
  sh "git push origin #{VERSION}"
end

task :publish => [:tests, :tag] do
  virtual_env("python setup.py sdist upload")
end
