# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git gunicorn
    [[ -d ~/.pyenv ]] && git -C ~/.pyenv pull || git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    [[ -f ~/.pyprofile ]] && rm -f ~/.pyprofile 
    touch ~/.pyprofile
    grep -qF -- 'source ~/.pyprofile' ~/.profile || echo 'source ~/.pyprofile' >> ~/.profile
    PYPROFILE='export PYENV_ROOT="$HOME/.pyenv"\nexport PATH="$PYENV_ROOT/bin:$PATH"\nexport PATH="~/.local/bin:$PATH"'
    grep -qF --  "$PYPROFILE" ~/.pyprofile || echo  "$PYPROFILE" >> ~/.pyprofile
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.pyprofile
    source ~/.profile
    pyenv install 3.7.6
    pyenv global 3.7.6
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    SHELL

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
    cd /vagrant
    source .env 
    poetry env use 3.7.6
    poetry install
    poetry run gunicorn --daemon --bind 0.0.0.0:5000 wsgi:app"}
  end
end
