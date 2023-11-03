echo "compile verilog with iverilog"
cp $1/code.txt ./code.txt
find ../src -name "*.v" | xargs iverilog -o $1/wave
echo "generate wave file"
vvp -n $1/wave -lxt2 > $1/cpu_output.txt
mv ./wave.vcd $1/wave.vcd
rm ./code.txt