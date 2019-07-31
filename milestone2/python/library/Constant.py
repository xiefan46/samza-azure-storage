#size
B = 1
KB = 1024 * B
MB = 1024 * KB
GB = 1024 * MB
TB = 1024 * GB

#test result
LOG_RES_P50 = "P50"
LOG_RES_P75 = "P75"
LOG_RES_P99 = "P99"
LOG_RES_P999 = "P99.9"
LOG_RES_P9999 = "P99.99"
LOG_RES_MICORS_OP = "micros/op"
LOG_RES_OPS_SEC = "ops/sec"
LOG_RES_RES_LINE = "Result Line"
LOG_RES_DELAY_LINE = "Delay Line"
LOG_RES_THROUGHPUT = "MB/s"

#test case config
CONFIG_KEY_SIZE = "KeySize"
CONFIG_VALUE_SIZE = "ValueSize"
CONFIG_VM_CACHE_MODE = "VMCacheMode"
CONFIG_TEST_CASE_NAME = "TestCaseName"
CONFIG_ROCKSDB_PARAMETERS = "RocksDB_Parameters"

#dir and file name
PERFORMANCE_RES_DIR_NAME = "performance-testing-log"
PERFORMANCE_RESULT_POSTFIX = "performance-result"


#Benchmark Parameters
parameter_bulkload = f"--disable_auto_compactions=1 \
                       --sync=0 \
                       --threads=1 \
                       --memtablerep=vector \
                       --allow_concurrent_memtable_write=false \
                       --disable_wal=1 "