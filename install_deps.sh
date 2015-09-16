echo "this project uses: py-feed, which i cannot find on any pip install repo"
wget https://sourceforge.net/projects/salix-sbo/files/13.37/pyfeed/pyfeed-0.7.4.tar.gz
tar -zxvf pyfeed-0.7.4.tar.gz
cd pyfeed-0.7.4
sudo python setup.py install
