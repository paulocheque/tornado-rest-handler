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

def virtual_env(command, env="env")
  sh "source #{env}/bin/activate ; #{command}"
end

task :tests => [] do
  virtual_env("nosetests")
  virtual_env("nosetests", "env3")
  virtual_env("nosetests", "env32")
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
