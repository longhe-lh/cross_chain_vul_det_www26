# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: mint, withdraw
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: xDai
- **事件**: TokenDeposit1
  - 函数: relayTokens
  - 关键操作: require(_receiver != address(0)), require(_receiver != address(this)), require(_amount > 0), require(withinLimit(_amount))
- **事件**: TokenRedeem2
  - 函数: claimTokens
  - 关键操作: require(_token != address(erc20token())), claimValues(_token, _to)
### rel_chain: Relay Chain
- **事件**: mint
  - 函数: executeSignatures
  - 关键操作: Message.hasEnoughValidSignatures(message, signatures, validatorContract(), false);, if (withinExecutionLimit(amount)) {, setRelayedMessages(txHash, true);, require(onExecuteMessage(recipient, amount, txHash));, emit RelayedMessage(recipient, amount, txHash);
- **事件**: withdraw
  - 函数: executeSignaturesGSN
  - 关键操作: Message.hasEnoughValidSignatures(message, signatures, validatorContract(), false);, if (withinExecutionLimit(amount)) {, require(maxTokensFee <= amount);, require(contractAddress == address(this));, require(!relayedMessages(txHash));, setRelayedMessages(txHash, true);, require(onExecuteMessageGSN(recipient, amount, maxTokensFee));, emit RelayedMessage(recipient, amount, txHash);
### det_chain: Destination Chain
- **事件**: TokenWithdraw1
  - 函数: claimTokens
  - 关键操作: require(_token != address(daiToken()));, require(_token != address(cDaiToken()) || !isInterestEnabled(bridgedToken));, require(_token != address(compToken()) || !isInterestEnabled(bridgedToken));, claimValues(_token, _to);
- **事件**: TokenMint2
  - 函数: onExecuteMessage
  - 关键操作: addTotalExecutedPerDay(getCurrentDay(), _amount);, ERC20 token = daiToken();, ensureEnoughTokens(token, _amount);, return token.transfer(_recipient, _amount);
---
