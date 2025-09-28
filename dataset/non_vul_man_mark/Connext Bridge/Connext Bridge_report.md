# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenDepositAndSwap2
- **rel_chain**: Dispatch
- **det_chain**: TokenWithdraw1, TokenMintAndSwap2
### src_chain: source_chain
- **事件**: TokenDeposit1
  - 函数: handleIncomingAsset
  - 关键操作: require(block.timestamp >= self.initialATime + Constants.MIN_RAMP_DELAY, "Wait 1 day before starting ramp"), require(futureTime_ >= block.timestamp + Constants.MIN_RAMP_TIME, "Insufficient ramp time"), require(futureA_ != 0 && futureA_ < Constants.MAX_A, "futureA_ must be > 0 and < MAX_A")
- **事件**: TokenDepositAndSwap2
  - 函数: swapToLocalAssetIfNeeded
  - 关键操作: if (_amount == 0) { return 0; }, if (_local == _asset) { return _amount; }
### rel_chain: relay_chain
- **事件**: Dispatch
  - 函数: dispatch
### det_chain: destination_chain
- **事件**: TokenWithdraw1
  - 函数: handleOutgoingAsset
  - 关键操作: if (_amount == 0) { return; }, SafeERC20.safeTransfer(IERC20Metadata(_asset), _to, _amount);
- **事件**: TokenMintAndSwap2
  - 函数: swapFromLocalAssetIfNeeded
  - 关键操作: if (adopted == _asset) { return (_amount, adopted); }, if (adopted == _asset) { return (_amount, adopted); }
---
