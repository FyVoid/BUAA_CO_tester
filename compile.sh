echo "compile verilog with iverilog"
find ../src -name "*.v" | xargs iverilog -o wave
echo "generate wave file"
vvp -n wave -lxt2 > cpu_output.txt
