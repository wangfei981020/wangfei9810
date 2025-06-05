log = """
log_error_count{namespace="g32-wallet", container="wallet-client-backend",tid="f0800f4f-a97a-465d-8aaa-98b7afbdb4c0", code="1354", msg="Transaction failed.",Exception="2024-11-27 03:27:51.199 tid:f0800f4f-a97a-465d-8aaa-98b7afbdb4c0 ERROR c.sl.wallet.mq.consumer.TransactionRetryReceptor.lambda$transactionRetry$0(59) - {"code":"1354","msg":"Transaction failed."}
com.sl.exceptions.UserWalletException: {"code":"1354","msg":"Transaction failed."}
        at com.sl.service.impl.TransactionServiceImpl.checkTransactions(TransactionServiceImpl.java:234)
        at com.sl.service.impl.TransactionServiceImpl.transaction(TransactionServiceImpl.java:189)
        at com.sl.service.impl.TransactionRetryServiceImpl.retry(TransactionRetryServiceImpl.java:72)
        at com.sl.wallet.mq.consumer.TransactionRetryReceptor.lambda$transactionRetry$0(TransactionRetryReceptor.java:57)
        at org.springframework.cloud.function.context.catalog.SimpleFunctionRegistry$FunctionInvocationWrapper.invokeConsumer(SimpleFunctionRegistry.java:1024)
        at org.springfra} 1
"""

log_data_bytes = log.encode('utf-8')
log_data_length = len(log_data_bytes)
print(log_data_length)
# 2. 如果字节数超过1020，则进行裁剪
# if log_data_length > max_length:
#     # 找到最后一个 `}` 的位置
#     last_brace_pos = log.rfind('}')