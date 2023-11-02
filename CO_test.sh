echo "generate random assembly program"
python generate.py

sh assemble.sh

sh compile.sh

echo "pairing verilog output with assembly program"
python analyse.py
echo "showing log"
cat log.txt

echo "opening GTKWave"
gtkwave wave.vcd
echo 'gtkwave exited'


echo 'deleting generated files'
rm wave.vcd
rm wave
echo 'generated files removed'