# 跨链桥合约分析报告
## 跨链桥: OmniBridge
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: mint, withdraw
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: source chain
- **事件**: TokenDeposit1
  - 函数: relayTokens
  - 关键操作: require(_receiver != address(0));, require(_receiver != address(this));, require(_amount > 0);, require(withinLimit(_amount));, addTotalSpentPerDay(getCurrentDay(), _amount);, erc20token().transferFrom(msg.sender, address(this), _amount);, emit UserRequestForAffirmation(_receiver, _amount);
- **事件**: TokenRedeem2
  - 函数: claimTokens
  - 关键操作: require(_token != address(erc20token()));, claimValues(_token, _to);
### rel_chain: relay chain
- **事件**: mint
  - 函数: executeSignatures
  - 关键操作: Message.hasEnoughValidSignatures(message, signatures, validatorContract(), false);, if (withinExecutionLimit(amount)) { require(contractAddress == address(this)); setRelayedMessages(txHash, true); require(onExecuteMessage(recipient, amount, txHash)); emit RelayedMessage(recipient, amount, txHash); } else { onFailedMessage(recipient, amount, txHash); }
- **事件**: withdraw
  - 函数: onFailedMessage
  - 关键操作: revert();
### det_chain: destination chain
- **事件**: TokenWithdraw1
  - 函数: claimTokens
  - 关键操作: require(_token != address(daiToken()));, require(_token != address(cDaiToken()) || !isInterestEnabled(bridgedToken));, require(_token != address(compToken()) || !isInterestEnabled(bridgedToken));, claimValues(_token, _to);
- **事件**: TokenMint2
  - 函数: onExecuteMessageGSN
  - 关键操作: ERC20 token = erc20token();, bool first = token.transfer(addressStorage[PAYMASTER], fee);, bool second = token.transfer(recipient, amount - fee);, return first && second;
---
