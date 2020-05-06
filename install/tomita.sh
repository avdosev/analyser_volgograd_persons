cd ~
git clone https://github.com/yandex/tomita-parser
cd tomita-parser && mkdir build && cd build
cmake ../src/ -DCMAKE_BUILD_TYPE=Release
make

# выполняем из папаки билд
wget https://github.com/yandex/tomita-parser/releases/download/v1.0/libmystem_c_binding.so.linux_x64.zip
unzip libmystem_c_binding.so.linux_x64.zip
export PATH="$HOME/tomita-parser/build/bin:$PATH"
source ~/.bashrc
