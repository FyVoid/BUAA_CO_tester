SHOW_WAVE="true"
SHOW_LOG="true"
SAVE_LOG="true"
RESULT_DIR="result"
SHOW_FIRST="false"
GENERATE_ASSEMBLY="true"
DELAY_SLOT="false"

index=1
for arg in $*
    do
    if [ $arg = "nw" ]
        then
        SHOW_WAVE="false"
    elif [ $arg = "nl" ]
        then 
        SAVE_LOG="false"
    elif [ $arg = "ns" ]
        then
        SHOW_LOG="false"
    elif [ $arg = "dir" ]
        then
        let index+=1
        eval j=\$$index
        RESULT_DIR=$j
    elif [ $arg = "sf" ]
        then
        SHOW_FIRST="true"
    elif [ $arg = "ng" ]
        then
        GENERATE_ASSEMBLY="false"
    elif [ $arg = "ds" ]
        then
        DELAY_SLOT="true"
    fi
    let index+=1
done

if [ $GENERATE_ASSEMBLY = "true" ]
    then
    echo "generate random assembly program"
    python generate.py ${RESULT_DIR}
else
    cp assemble.asm ${RESULT_DIR}/assemble.asm
fi

if [ $DELAY_SLOT = "true" ]
    then
    echo "assemble with delay slot enabled"
    sh assemble.sh ${RESULT_DIR} ds
else
    sh assemble.sh ${RESULT_DIR}
fi

sh compile.sh ${RESULT_DIR}

echo "pairing verilog output with assembly program"
python analyse.py ${RESULT_DIR} "sl:${SAVE_LOG}" "sf:${SHOW_FIRST}"
if [ $SHOW_LOG = "true" ]
    then
    echo "showing log"
    cat ${RESULT_DIR}/log.txt
fi

if [ $SHOW_WAVE = "true" ]
    then
    echo "opening GTKWave"
    gtkwave ${RESULT_DIR}/wave.vcd
    echo 'gtkwave exited'
fi

echo 'deleting generated files'
rm ${RESULT_DIR}/wave.vcd
rm ${RESULT_DIR}/wave
echo 'generated files removed'
