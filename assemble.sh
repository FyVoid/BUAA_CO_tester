DELAY_SLOT="false"

for arg in $*
    do
    if [ $arg = "ds" ]
        then
        DELAY_SLOT="true"
    fi
done

if [ $DELAY_SLOT = "true" ]
    then
    echo "assemble and dump generated assmbly program into code.txt"
    java -jar CO_mars.jar db nc a mc CompactLargeText dump .text HexText $1/code.txt $1/assemble.asm

    echo "run assemble.asm with CS_mars to generate std_output.txt"
    java -jar CO_mars.jar db nc $1/assemble.asm mc CompactLargeText coL1 ig 5500 > $1/std_output.txt

else
    echo "assemble and dump generated assmbly program into code.txt"
    java -jar CO_mars.jar nc a mc CompactLargeText dump .text HexText $1/code.txt $1/assemble.asm

    echo "run assemble.asm with CS_mars to generate std_output.txt"
    java -jar CO_mars.jar nc $1/assemble.asm mc CompactLargeText coL1 ig 5500 > $1/std_output.txt
fi


