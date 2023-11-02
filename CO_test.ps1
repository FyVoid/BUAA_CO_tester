Write-Output "powershell命令是真的又难用又丑"
Write-Output "generate random assembly program"
python generate.py

assemble.ps1

compile.ps1

Write-Output "pairing verilog output with assembly program"
python analyse.py
Write-Output "showing log"
cat log.txt

Write-Output "opening GTKWave"
gtkwave wave.vcd
Write-Output 'gtkwave exited'


Write-Output 'deleting generated files'
Remove-Item wave.vcd
Remove-Item wave
Write-Output 'generated files removed'