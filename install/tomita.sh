cd ~
git clone https://github.com/yandex/tomita-parser
cd tomita-parser && mkdir build && cd build
cmake ../src/ -DCMAKE_BUILD_TYPE=Release
make

