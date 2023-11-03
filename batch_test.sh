BATCH=50
BATCH_DIR="result"
RESULT_DIR="test_batch"

if [ $# -gt 0 ]
    then
    BATCH=$1
fi

rm -rf $RESULT_DIR
mkdir $RESULT_DIR

for ((i=0; i<BATCH; i++))
    do
    echo "test ${i}"
    dirname="${BATCH_DIR}-${i}"
    sh CO_test.sh nw nl ns dir ${dirname} > stdout.txt
    mv -f ${dirname} $RESULT_DIR
    mv -f stdout.txt "${RESULT_DIR}/${dirname}"
    echo "test ${i} completed"
done

python batch_analyse.py $RESULT_DIR $BATCH_DIR $BATCH

cat batch_log.txt