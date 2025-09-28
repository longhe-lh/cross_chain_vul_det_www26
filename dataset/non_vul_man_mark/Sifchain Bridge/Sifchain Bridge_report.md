# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: LogLock1, LogBurn2
- **rel_chain**: NewProphecyClaim, ProphecyCompleted
- **det_chain**: LogBridgeTokenMint1, LogUnlock2
### src_chain: Ethereum
- **事件**: LogLock1
  - 函数: lock
  - 关键操作: require(_amount > maxTokenAmount[symbol], "Amount being transferred is over the limit");, tokenToTransfer.safeTransferFrom(msg.sender, address(this), _amount);
- **事件**: LogBurn2
  - 函数: burn
  - 关键操作: if (_amount > maxTokenAmount[symbol]) { revert("Amount being transferred is over the limit for this token"); }, BridgeToken(_token).burnFrom(msg.sender, _amount);
### rel_chain: RelayChain
- **事件**: NewProphecyClaim
  - 函数: newProphecyClaim
  - 关键操作: require(oracleClaimValidators[_prophecyID] == 0, "Already processed prophecy claim");, completeProphecyClaim(_prophecyID, tokenAddress, claimType, _ethereumReceiver, _symbol, _amount);
- **事件**: ProphecyCompleted
  - 函数: completeProphecyClaim
### det_chain: Cosmos
- **事件**: LogBridgeTokenMint1
  - 函数: mintNewBridgeTokens
  - 关键操作: require(BridgeToken(_bridgeTokenAddress).mint(_intendedRecipient, _amount), "Attempted mint of bridge tokens failed");
- **事件**: LogUnlock2
  - 函数: unlockFunds
  - 关键操作: lockedFunds[_token] = lockedFunds[_token].sub(_amount);, (bool success,) = _recipient.call.value(_amount)(""); require(success, "error sending ether");, tokenToTransfer.safeTransfer(_recipient, _amount);
---
