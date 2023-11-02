echo "assemble and dump generated assmbly program into code.txt"
java -jar CO_mars.jar nc a mc CompactLargeText dump .text HexText code.txt assemble.asm

echo "run assemble.asm with CS_mars to generate std_output.txt"
java -jar CO_mars.jar nc assemble.asm mc CompactLargeText coL1 ig 1000 > std_output.txt