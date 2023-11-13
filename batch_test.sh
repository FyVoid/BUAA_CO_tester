BATCH=50
BATCH_DIR="result"
RESULT_DIR="test_batch"
DELAY_SLOT="false"

if [ $# -gt 0 ]
    then
    BATCH=$1
fi

for arg in $*
    do
    if [ $arg = "ds" ]
        then
        DELAY_SLOT="true"
    fi
done

rm -rf $RESULT_DIR
mkdir $RESULT_DIR

for ((i=0; i<BATCH; i++))
    do
    echo "test ${i}"
    dirname="${BATCH_DIR}-${i}"
    if [ $DELAY_SLOT = "false" ]
        then
        sh CO_test.sh nw nl ns sf dir ${dirname} > stdout.txt
    else
        sh CO_test.sh nw nl ns ds sf dir ${dirname} > stdout.txt
    fi
    mv -f ${dirname} $RESULT_DIR
    mv -f stdout.txt "${RESULT_DIR}/${dirname}"
    echo "completed"
done

python batch_analyse.py $RESULT_DIR $BATCH_DIR $BATCH

cat batch_log.txt