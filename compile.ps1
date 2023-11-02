Write-Output "compile verilog with iverilog"
Get-ChildItem -Path ..\src\*.v | xargs iverilog -o wave

Write-Output "generate wave file"
vvp -n wave -lxt2 > cpu_output.txt
